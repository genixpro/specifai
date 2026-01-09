import uuid

from sqlmodel import Session

from specifai.items.backend.data_repository.item_data_repository_postgres import (
    PostgresItemDataRepository,
)
from specifai.items.backend.data_models.item_models import Item, ItemCreate


def create_item(
    *,
    session: Session,
    item_in: ItemCreate,
    owner_id: uuid.UUID,
    workspace_id: uuid.UUID | None,
) -> Item:
    repo = PostgresItemDataRepository(session)
    return repo.create_item(
        item_in=item_in, owner_id=owner_id, workspace_id=workspace_id
    )
