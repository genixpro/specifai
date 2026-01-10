from __future__ import annotations

import uuid
from typing import Any

from sqlmodel import Session, col, delete, func, select

from specifai.items.backend.data_models.item_models import Item, ItemCreate
from specifai.items.backend.data_repository.item_data_repository_base import (
    ItemDataRepository,
)


class PostgresItemDataRepository(ItemDataRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_item_by_id(self, item_id: uuid.UUID) -> Item | None:
        return self._session.get(Item, item_id)

    def list_items(
        self,
        *,
        owner_id: uuid.UUID | None,
        workspace_id: uuid.UUID | None,
        skip: int,
        limit: int,
    ) -> tuple[list[Item], int]:
        count_statement = select(func.count()).select_from(Item)
        statement = select(Item)
        if owner_id is not None:
            count_statement = count_statement.where(Item.owner_id == owner_id)
            statement = statement.where(Item.owner_id == owner_id)
        if workspace_id is not None:
            count_statement = count_statement.where(Item.workspace_id == workspace_id)
            statement = statement.where(Item.workspace_id == workspace_id)
        count = self._session.exec(count_statement).one()
        items = self._session.exec(statement.offset(skip).limit(limit)).all()
        return list(items), count

    def create_item(
        self,
        *,
        item_in: ItemCreate,
        owner_id: uuid.UUID,
        workspace_id: uuid.UUID | None,
    ) -> Item:
        db_item = Item.model_validate(
            item_in, update={"owner_id": owner_id, "workspace_id": workspace_id}
        )
        self._session.add(db_item)
        self._session.commit()
        self._session.refresh(db_item)
        return db_item

    def update_item(self, *, item: Item, update_data: dict[str, Any]) -> Item:
        item.sqlmodel_update(update_data)
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def delete_item(self, *, item: Item) -> None:
        self._session.delete(item)
        self._session.commit()

    def delete_items_for_user(self, *, user_id: uuid.UUID) -> None:
        statement = delete(Item).where(col(Item.owner_id) == user_id)
        self._session.exec(statement)  # type: ignore
