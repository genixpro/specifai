from collections.abc import Generator
import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, delete
from sqlalchemy.pool import StaticPool

from specifai.general.backend.components.config import settings
from specifai.general.backend.components import db as db_module
from specifai.general.backend.apis import deps as deps_module
from specifai.general.backend.components.db import init_db
from specifai.general.backend.components.main import app
from specifai.items.backend.data_models.item_models import Item
from specifai.users.backend.components.user_test_utils import (
    authentication_token_from_email,
)
from specifai.users.backend.data_models.user_models import User
from specifai.workspaces.backend.data_models.workspace_models import Workspace
from specifai.general.backend.utils.test_utils import get_superuser_token_headers


def _build_test_engine():
    test_db_url = os.getenv("TEST_DATABASE_URL")
    if test_db_url:
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
    if os.getenv("TEST_DATABASE_URL") is None:
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
