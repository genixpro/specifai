from sqlmodel import Session

from specifai.general.backend.utils.test_utils import random_email, random_lower_string
from specifai.users.backend.data_models.user_models import UserCreate
from specifai.users.backend.data_repository.user_data_repository_postgres import (
    PostgresUserDataRepository,
)
from specifai.workspaces.backend.data_models.workspace_models import WorkspaceCreate
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)


def test_workspace_repository_crud(db: Session) -> None:
    user_repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)

    user = user_repo.create_user(
        user_create=UserCreate(email=random_email(), password=random_lower_string())
    )
    workspace = workspace_repo.create_workspace(
        workspace_in=WorkspaceCreate(name="Alpha"), owner_id=user.id
    )
    assert workspace.id

    fetched = workspace_repo.get_workspace_by_id(workspace.id)
    assert fetched
    assert fetched.name == "Alpha"

    workspaces, count = workspace_repo.list_workspaces(
        owner_id=user.id, skip=0, limit=100
    )
    assert count >= 1
    assert any(db_workspace.id == workspace.id for db_workspace in workspaces)

    updated = workspace_repo.update_workspace(
        workspace=workspace, update_data={"name": "Beta"}
    )
    assert updated.name == "Beta"

    workspace_repo.delete_workspace(workspace=updated)
    assert workspace_repo.get_workspace_by_id(updated.id) is None


def test_workspace_repository_default_workspace(db: Session) -> None:
    user_repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)

    user = user_repo.create_user(
        user_create=UserCreate(email=random_email(), password=random_lower_string())
    )
    default_workspace = workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert default_workspace.name == "Personal"

    same_workspace = workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert same_workspace.id == default_workspace.id
