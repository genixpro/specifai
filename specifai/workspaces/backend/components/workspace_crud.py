import uuid

from sqlmodel import Session

from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)
from specifai.workspaces.backend.data_models.workspace_models import (
    Workspace,
    WorkspaceCreate,
)


def create_workspace(
    *, session: Session, workspace_in: WorkspaceCreate, owner_id: uuid.UUID
) -> Workspace:
    repo = PostgresWorkspaceDataRepository(session)
    return repo.create_workspace(workspace_in=workspace_in, owner_id=owner_id)


def get_workspaces_for_owner(
    *, session: Session, owner_id: uuid.UUID
) -> list[Workspace]:
    repo = PostgresWorkspaceDataRepository(session)
    workspaces, _count = repo.list_workspaces(
        owner_id=owner_id, skip=0, limit=10_000
    )
    return workspaces


def get_or_create_default_workspace(
    *, session: Session, owner_id: uuid.UUID
) -> Workspace:
    repo = PostgresWorkspaceDataRepository(session)
    return repo.get_or_create_default_workspace(owner_id=owner_id)
