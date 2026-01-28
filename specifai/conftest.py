import os
from collections.abc import Generator
from typing import Any

import mongomock
import pytest
from fastapi.testclient import TestClient
from pymongo.database import Database

from specifai.general.backend.components import db as db_module
from specifai.general.backend.components.config import settings
from specifai.general.backend.components.db import init_db
from specifai.general.backend.components.main import app
from specifai.general.backend.utils.test_utils import get_superuser_token_headers
from specifai.users.backend.components.user_test_utils import (
    authentication_token_from_email,
)

os.environ.setdefault("BACKEND_PRESTART_MAX_TRIES", "1")
os.environ.setdefault("BACKEND_PRESTART_WAIT_SECONDS", "0")
os.environ.setdefault("BACKEND_PRESTART_RERAISE", "1")

WORKER_ID = os.getenv("PYTEST_XDIST_WORKER", "gw0")
TEST_DB_NAME = f"specifai_test_{WORKER_ID}"

mongo_client = mongomock.MongoClient()
db_module.mongo_client = mongo_client
db_module.mongo_db = mongo_client[TEST_DB_NAME]


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Database[dict[str, Any]], None, None]:
    db = db_module.get_database()
    init_db(db)
    yield db
    mongo_client.drop_database(TEST_DB_NAME)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(
    client: TestClient, db: Database[dict[str, Any]]
) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
