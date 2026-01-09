from __future__ import annotations

from typing import Any
import uuid

from sqlmodel import Session, func, select

from specifai.workspaces.backend.data_repository.workspace_data_repository_base import (
    WorkspaceDataRepository,
)
from specifai.workspaces.backend.data_models.workspace_models import (
    Workspace,
    WorkspaceCreate,
)


class PostgresWorkspaceDataRepository(WorkspaceDataRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_workspace_by_id(self, workspace_id: uuid.UUID) -> Workspace | None:
        return self._session.get(Workspace, workspace_id)

    def list_workspaces(
        self, *, owner_id: uuid.UUID | None, skip: int, limit: int
    ) -> tuple[list[Workspace], int]:
        count_statement = select(func.count()).select_from(Workspace)
        statement = select(Workspace)
        if owner_id is not None:
            count_statement = count_statement.where(Workspace.owner_id == owner_id)
            statement = statement.where(Workspace.owner_id == owner_id)
        count = self._session.exec(count_statement).one()
        workspaces = self._session.exec(statement.offset(skip).limit(limit)).all()
        return list(workspaces), count

    def create_workspace(
        self, *, workspace_in: WorkspaceCreate, owner_id: uuid.UUID
    ) -> Workspace:
        db_workspace = Workspace.model_validate(
            workspace_in, update={"owner_id": owner_id}
        )
        self._session.add(db_workspace)
        self._session.commit()
        self._session.refresh(db_workspace)
        return db_workspace

    def update_workspace(
        self, *, workspace: Workspace, update_data: dict[str, Any]
    ) -> Workspace:
        workspace.sqlmodel_update(update_data)
        self._session.add(workspace)
        self._session.commit()
        self._session.refresh(workspace)
        return workspace

    def delete_workspace(self, *, workspace: Workspace) -> None:
        self._session.delete(workspace)
        self._session.commit()

    def get_or_create_default_workspace(
        self, *, owner_id: uuid.UUID
    ) -> Workspace:
        statement = (
            select(Workspace)
            .where(Workspace.owner_id == owner_id)
            .order_by(Workspace.name.asc())
        )
        workspace = self._session.exec(statement).first()
        if workspace:
            return workspace
        workspace_in = WorkspaceCreate(name="Personal")
        return self.create_workspace(workspace_in=workspace_in, owner_id=owner_id)
