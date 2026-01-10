from unittest.mock import MagicMock

import pytest

from specifai.workspaces.backend.data_repository.workspace_data_repository_base import (
    WorkspaceDataRepository,
)


class DummyWorkspaceRepository(WorkspaceDataRepository):
    def get_workspace_by_id(self, workspace_id):
        return super().get_workspace_by_id(workspace_id)

    def list_workspaces(self, *, owner_id, skip, limit):
        return super().list_workspaces(owner_id=owner_id, skip=skip, limit=limit)

    def create_workspace(self, *, workspace_in, owner_id):
        return super().create_workspace(workspace_in=workspace_in, owner_id=owner_id)

    def update_workspace(self, *, workspace, update_data):
        return super().update_workspace(workspace=workspace, update_data=update_data)

    def delete_workspace(self, *, workspace):
        return super().delete_workspace(workspace=workspace)

    def get_or_create_default_workspace(self, *, owner_id):
        return super().get_or_create_default_workspace(owner_id=owner_id)


def test_workspace_data_repository_base_raises_not_implemented() -> None:
    repo = DummyWorkspaceRepository()
    with pytest.raises(NotImplementedError):
        repo.get_workspace_by_id(MagicMock())
    with pytest.raises(NotImplementedError):
        repo.list_workspaces(owner_id=None, skip=0, limit=1)
    with pytest.raises(NotImplementedError):
        repo.create_workspace(workspace_in=MagicMock(), owner_id=MagicMock())
    with pytest.raises(NotImplementedError):
        repo.update_workspace(workspace=MagicMock(), update_data={})
    with pytest.raises(NotImplementedError):
        repo.delete_workspace(workspace=MagicMock())
    with pytest.raises(NotImplementedError):
        repo.get_or_create_default_workspace(owner_id=MagicMock())
