import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from specifai.general.backend.apis.deps import CurrentUser, WorkspaceRepoDep
from specifai.general.backend.data_models.message_models import Message
from specifai.workspaces.backend.data_models.workspace_models import (
    WorkspaceCreate,
    WorkspacePublic,
    WorkspacesPublic,
    WorkspaceUpdate,
)

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("/", response_model=WorkspacesPublic)
def read_workspaces(
    repo: WorkspaceRepoDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve workspaces.
    """
    owner_id = None if current_user.is_superuser else current_user.id
    workspaces, count = repo.list_workspaces(owner_id=owner_id, skip=skip, limit=limit)
    public_workspaces = [
        WorkspacePublic.model_validate(workspace) for workspace in workspaces
    ]
    return WorkspacesPublic(data=public_workspaces, count=count)


@router.get("/{id}", response_model=WorkspacePublic)
def read_workspace(
    repo: WorkspaceRepoDep, current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get workspace by ID.
    """
    workspace = repo.get_workspace_by_id(id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    if not current_user.is_superuser and workspace.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return workspace


@router.post("/", response_model=WorkspacePublic)
def create_workspace(
    *,
    repo: WorkspaceRepoDep,
    current_user: CurrentUser,
    workspace_in: WorkspaceCreate,
) -> Any:
    """
    Create new workspace.
    """
    return repo.create_workspace(workspace_in=workspace_in, owner_id=current_user.id)


@router.put("/{id}", response_model=WorkspacePublic)
def update_workspace(
    *,
    repo: WorkspaceRepoDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    workspace_in: WorkspaceUpdate,
) -> Any:
    """
    Update a workspace.
    """
    workspace = repo.get_workspace_by_id(id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    if not current_user.is_superuser and workspace.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = workspace_in.model_dump(exclude_unset=True)
    return repo.update_workspace(workspace=workspace, update_data=update_dict)


@router.delete("/{id}")
def delete_workspace(
    repo: WorkspaceRepoDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a workspace.
    """
    workspace = repo.get_workspace_by_id(id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    if not current_user.is_superuser and workspace.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    repo.delete_workspace(workspace=workspace)
    return Message(message="Workspace deleted successfully")
