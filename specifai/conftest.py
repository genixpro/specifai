import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, delete

from specifai.general.backend.apis import deps as deps_module
from specifai.general.backend.components import db as db_module
from specifai.general.backend.components.config import settings
from specifai.general.backend.components.db import init_db
from specifai.general.backend.components.main import app
from specifai.general.backend.utils.test_utils import get_superuser_token_headers
from specifai.items.backend.data_models.item_models import Item
from specifai.users.backend.components.user_test_utils import (
    authentication_token_from_email,
)
from specifai.users.backend.data_models.user_models import User
from specifai.workspaces.backend.data_models.workspace_models import Workspace

os.environ.setdefault("BACKEND_PRESTART_MAX_TRIES", "1")
os.environ.setdefault("BACKEND_PRESTART_WAIT_SECONDS", "0")
os.environ.setdefault("BACKEND_PRESTART_RERAISE", "1")

WORKER_ID = os.getenv("PYTEST_XDIST_WORKER", "gw0")
TEST_DB_NAME: str | None = None
TEST_DB_ADMIN_URL: str | None = None


def _prepare_test_database(test_db_url: str) -> str:
    global TEST_DB_ADMIN_URL
    global TEST_DB_NAME

    url = make_url(test_db_url)
    if url.database in (None, "", ":memory:"):
        return str(url)

    if url.drivername.startswith("sqlite"):
        base, ext = os.path.splitext(url.database)
        database = f"{base}_{WORKER_ID}{ext}"
        return str(url.set(database=database))

    TEST_DB_NAME = f"{url.database}_{WORKER_ID}"
    TEST_DB_ADMIN_URL = str(url.set(database="postgres"))
    admin_engine = create_engine(TEST_DB_ADMIN_URL, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
        conn.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    admin_engine.dispose()
    return str(url.set(database=TEST_DB_NAME))


def _build_test_engine():
    test_db_url = os.getenv("TEST_DATABASE_URL")
    if test_db_url:
        test_db_url = _prepare_test_database(test_db_url)
        return create_engine(test_db_url)
    return create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


TEST_ENGINE = _build_test_engine()
db_module.engine = TEST_ENGINE
deps_module.engine = TEST_ENGINE


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(TEST_ENGINE)
    with Session(TEST_ENGINE) as session:
        init_db(session)
        yield session
        statement = delete(Item)
        session.execute(statement)
        statement = delete(Workspace)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()
    if TEST_DB_NAME and TEST_DB_ADMIN_URL:
        TEST_ENGINE.dispose()
        admin_engine = create_engine(TEST_DB_ADMIN_URL, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
        admin_engine.dispose()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
