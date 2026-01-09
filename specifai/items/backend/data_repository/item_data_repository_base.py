from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import uuid

from specifai.items.backend.data_models.item_models import Item, ItemCreate


class ItemDataRepository(ABC):
    @abstractmethod
    def get_item_by_id(self, item_id: uuid.UUID) -> Item | None:
        raise NotImplementedError

    @abstractmethod
    def list_items(
        self,
        *,
        owner_id: uuid.UUID | None,
        workspace_id: uuid.UUID | None,
        skip: int,
        limit: int,
    ) -> tuple[list[Item], int]:
        raise NotImplementedError

    @abstractmethod
    def create_item(
        self,
        *,
        item_in: ItemCreate,
        owner_id: uuid.UUID,
        workspace_id: uuid.UUID | None,
    ) -> Item:
        raise NotImplementedError

    @abstractmethod
    def update_item(self, *, item: Item, update_data: dict[str, Any]) -> Item:
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, *, item: Item) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_items_for_user(self, *, user_id: uuid.UUID) -> None:
        raise NotImplementedError
