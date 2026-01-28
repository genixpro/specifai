import uuid

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class Workspace(WorkspaceBase):
    model_config = ConfigDict(extra="allow")
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    owner_id: uuid.UUID


class WorkspacePublic(WorkspaceBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    owner_id: uuid.UUID


class WorkspacesPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[WorkspacePublic]
    count: int
