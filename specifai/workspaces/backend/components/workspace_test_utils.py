from sqlmodel import Session

from specifai.general.backend.utils.test_utils import random_lower_string
from specifai.users.backend.components.user_test_utils import create_random_user
from specifai.workspaces.backend.data_models.workspace_models import (
    Workspace,
    WorkspaceCreate,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)


def create_random_workspace(db: Session) -> Workspace:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    workspace_in = WorkspaceCreate(name=random_lower_string())
    repo = PostgresWorkspaceDataRepository(db)
    return repo.create_workspace(workspace_in=workspace_in, owner_id=owner_id)
