import uuid

from pydantic import BaseModel, ConfigDict, Field

# Shared properties
class ItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    workspace_id: uuid.UUID | None = Field(
        default=None
    )


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase):
    model_config = ConfigDict(extra="allow")
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[ItemPublic]
    count: int
