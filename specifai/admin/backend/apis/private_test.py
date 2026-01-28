import uuid
from typing import Any

from fastapi.testclient import TestClient
from pymongo.database import Database

from specifai.general.backend.components.config import settings
from specifai.users.backend.data_repository.user_data_repository_mongo import (
    MongoUserDataRepository,
)


def test_create_user(client: TestClient, db: Database[dict[str, Any]]) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/private/users/",
        json={
            "email": "pollo@listo.com",
            "password": "password123",
            "full_name": "Pollo Listo",
        },
    )

    assert r.status_code == 200

    data = r.json()

    user_id = uuid.UUID(data["id"])
    repo = MongoUserDataRepository(db)
    user = repo.get_user_by_id(user_id)

    assert user
    assert user.email == "pollo@listo.com"
    assert user.full_name == "Pollo Listo"
