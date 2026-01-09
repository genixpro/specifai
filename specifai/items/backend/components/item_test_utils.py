from sqlmodel import Session

from specifai.items.backend.data_repository.item_data_repository_postgres import (
    PostgresItemDataRepository,
)
from specifai.items.backend.data_models.item_models import Item, ItemCreate
from specifai.users.backend.components.user_test_utils import create_random_user
from specifai.general.backend.utils.test_utils import random_lower_string
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    workspace_repo = PostgresWorkspaceDataRepository(db)
    workspace = workspace_repo.get_or_create_default_workspace(owner_id=owner_id)
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(
        title=title, description=description, workspace_id=workspace.id
    )
    repo = PostgresItemDataRepository(db)
    return repo.create_item(
        item_in=item_in, owner_id=owner_id, workspace_id=workspace.id
    )
