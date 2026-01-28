from __future__ import annotations

import uuid
from collections.abc import Iterable
from typing import Any

from pymongo.database import Database

from specifai.items.backend.data_models.item_models import Item, ItemCreate
from specifai.items.backend.data_repository.item_data_repository_base import (
    ItemDataRepository,
)


class MongoItemDataRepository(ItemDataRepository):
    def __init__(self, db: Database[dict[str, Any]]) -> None:
        self._collection = db["items"]

    def get_item_by_id(self, item_id: uuid.UUID) -> Item | None:
        doc = self._collection.find_one({"_id": str(item_id)})
        return self._doc_to_item(doc)

    def list_items(
        self,
        *,
        owner_id: uuid.UUID | None,
        workspace_id: uuid.UUID | None,
        skip: int,
        limit: int,
    ) -> tuple[list[Item], int]:
        query: dict[str, Any] = {}
        if owner_id is not None:
            query["owner_id"] = str(owner_id)
        if workspace_id is not None:
            query["workspace_id"] = str(workspace_id)
        count = self._collection.count_documents(query)
        cursor = self._collection.find(query).skip(skip).limit(limit)
        return self._cursor_to_items(cursor), count

    def create_item(
        self,
        *,
        item_in: ItemCreate,
        owner_id: uuid.UUID,
        workspace_id: uuid.UUID | None,
    ) -> Item:
        item_data = item_in.model_dump()
        item_data["owner_id"] = owner_id
        item_data["workspace_id"] = workspace_id
        item = Item(**item_data)
        self._collection.insert_one(self._item_to_doc(item))
        return item

    def update_item(self, *, item: Item, update_data: dict[str, Any]) -> Item:
        update_payload = self._serialize_item_update(update_data)
        if update_payload:
            self._collection.update_one({"_id": str(item.id)}, {"$set": update_payload})
        refreshed = self.get_item_by_id(item.id)
        if refreshed is None:
            raise ValueError("Item not found after update")
        return refreshed

    def delete_item(self, *, item: Item) -> None:
        self._collection.delete_one({"_id": str(item.id)})

    def delete_items_for_user(self, *, user_id: uuid.UUID) -> None:
        self._collection.delete_many({"owner_id": str(user_id)})

    def _serialize_item_update(self, update_payload: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for key, value in update_payload.items():
            if value is None:
                payload[key] = None
            elif isinstance(value, uuid.UUID):
                payload[key] = str(value)
            else:
                payload[key] = value
        return payload

    def _item_to_doc(self, item: Item) -> dict[str, Any]:
        data = item.model_dump()
        data["_id"] = str(data.pop("id"))
        return self._serialize_item_update(data)

    def _doc_to_item(self, doc: dict[str, Any] | None) -> Item | None:
        if not doc:
            return None
        data = dict(doc)
        data["id"] = uuid.UUID(str(data.pop("_id")))
        if "owner_id" in data and data["owner_id"] is not None:
            data["owner_id"] = uuid.UUID(str(data["owner_id"]))
        if "workspace_id" in data and data["workspace_id"] is not None:
            data["workspace_id"] = uuid.UUID(str(data["workspace_id"]))
        return Item.model_validate(data)

    def _cursor_to_items(self, cursor: Iterable[dict[str, Any]]) -> list[Item]:
        items: list[Item] = []
        for doc in cursor:
            item = self._doc_to_item(doc)
            if item:
                items.append(item)
        return items
