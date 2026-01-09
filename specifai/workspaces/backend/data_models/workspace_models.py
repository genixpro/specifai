import uuid
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from specifai.items.backend.data_models.item_models import Item
    from specifai.users.backend.data_models.user_models import User


class WorkspaceBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class Workspace(WorkspaceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="workspaces")
    items: list["Item"] = Relationship(back_populates="workspace", cascade_delete=True)


class WorkspacePublic(WorkspaceBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class WorkspacesPublic(SQLModel):
    data: list[WorkspacePublic]
    count: int
