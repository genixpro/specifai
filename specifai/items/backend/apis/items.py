import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from specifai.general.backend.apis.deps import (
    CurrentUser,
    ItemRepoDep,
    WorkspaceRepoDep,
)
from specifai.general.backend.data_models.message_models import Message
from specifai.items.backend.data_models.item_models import (
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsPublic)
def read_items(
    item_repo: ItemRepoDep,
    workspace_repo: WorkspaceRepoDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    workspace_id: uuid.UUID | None = None,
) -> Any:
    """
    Retrieve items.
    """

    if current_user.is_superuser:
        items, count = item_repo.list_items(
            owner_id=None,
            workspace_id=workspace_id,
            skip=skip,
            limit=limit,
        )
    else:
        if workspace_id:
            workspace = workspace_repo.get_workspace_by_id(workspace_id)
            if not workspace or workspace.owner_id != current_user.id:
                raise HTTPException(status_code=404, detail="Workspace not found")
        items, count = item_repo.list_items(
            owner_id=current_user.id,
            workspace_id=workspace_id,
            skip=skip,
            limit=limit,
        )

    return ItemsPublic(data=items, count=count)


@router.get("/{id}", response_model=ItemPublic)
def read_item(item_repo: ItemRepoDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get item by ID.
    """
    item = item_repo.get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/", response_model=ItemPublic)
def create_item(
    *,
    item_repo: ItemRepoDep,
    workspace_repo: WorkspaceRepoDep,
    current_user: CurrentUser,
    item_in: ItemCreate,
) -> Any:
    """
    Create new item.
    """
    workspace_id = item_in.workspace_id
    if workspace_id is None:
        default_workspace = workspace_repo.get_or_create_default_workspace(
            owner_id=current_user.id
        )
        workspace_id = default_workspace.id
    else:
        workspace = workspace_repo.get_workspace_by_id(workspace_id)
        if not workspace or (
            not current_user.is_superuser and workspace.owner_id != current_user.id
        ):
            raise HTTPException(status_code=404, detail="Workspace not found")
    return item_repo.create_item(
        item_in=item_in,
        owner_id=current_user.id,
        workspace_id=workspace_id,
    )


@router.put("/{id}", response_model=ItemPublic)
def update_item(
    *,
    item_repo: ItemRepoDep,
    workspace_repo: WorkspaceRepoDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = item_repo.get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    if "workspace_id" in update_dict and update_dict["workspace_id"]:
        workspace = workspace_repo.get_workspace_by_id(update_dict["workspace_id"])
        if not workspace or (
            not current_user.is_superuser and workspace.owner_id != current_user.id
        ):
            raise HTTPException(status_code=404, detail="Workspace not found")
    return item_repo.update_item(item=item, update_data=update_dict)


@router.delete("/{id}")
def delete_item(
    item_repo: ItemRepoDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an item.
    """
    item = item_repo.get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item_repo.delete_item(item=item)
    return Message(message="Item deleted successfully")
