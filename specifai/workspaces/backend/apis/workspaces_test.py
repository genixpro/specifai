import uuid
from typing import Any

from fastapi.testclient import TestClient
from pymongo.database import Database

from specifai.general.backend.components.config import settings
from specifai.workspaces.backend.components.workspace_test_utils import (
    create_random_workspace,
)


def test_create_workspace(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Engineering"}
    response = client.post(
        f"{settings.API_V1_STR}/workspaces/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content
    assert "owner_id" in content


def test_read_workspace(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    db: Database[dict[str, Any]],
) -> None:
    workspace = create_random_workspace(db)
    response = client.get(
        f"{settings.API_V1_STR}/workspaces/{workspace.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == workspace.name
    assert content["id"] == str(workspace.id)
    assert content["owner_id"] == str(workspace.owner_id)


def test_read_workspace_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/workspaces/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Workspace not found"


def test_read_workspace_not_enough_permissions(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Database[dict[str, Any]],
) -> None:
    workspace = create_random_workspace(db)
    response = client.get(
        f"{settings.API_V1_STR}/workspaces/{workspace.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_workspaces(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    db: Database[dict[str, Any]],
) -> None:
    create_random_workspace(db)
    create_random_workspace(db)
    response = client.get(
        f"{settings.API_V1_STR}/workspaces/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_delete_workspace(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    db: Database[dict[str, Any]],
) -> None:
    workspace = create_random_workspace(db)
    response = client.delete(
        f"{settings.API_V1_STR}/workspaces/{workspace.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Workspace deleted successfully"
