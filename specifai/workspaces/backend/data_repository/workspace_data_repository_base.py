from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any

from specifai.workspaces.backend.data_models.workspace_models import (
    Workspace,
    WorkspaceCreate,
)


class WorkspaceDataRepository(ABC):
    @abstractmethod
    def get_workspace_by_id(self, workspace_id: uuid.UUID) -> Workspace | None:
        raise NotImplementedError

    @abstractmethod
    def list_workspaces(
        self, *, owner_id: uuid.UUID | None, skip: int, limit: int
    ) -> tuple[list[Workspace], int]:
        raise NotImplementedError

    @abstractmethod
    def create_workspace(
        self, *, workspace_in: WorkspaceCreate, owner_id: uuid.UUID
    ) -> Workspace:
        raise NotImplementedError

    @abstractmethod
    def update_workspace(
        self, *, workspace: Workspace, update_data: dict[str, Any]
    ) -> Workspace:
        raise NotImplementedError

    @abstractmethod
    def delete_workspace(self, *, workspace: Workspace) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_or_create_default_workspace(self, *, owner_id: uuid.UUID) -> Workspace:
        raise NotImplementedError
