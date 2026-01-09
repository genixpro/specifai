from specifai.workspaces.backend.data_repository.workspace_data_repository_base import (
    WorkspaceDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)

__all__ = ["PostgresWorkspaceDataRepository", "WorkspaceDataRepository"]
