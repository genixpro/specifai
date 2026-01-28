from typing import Any

from pymongo.database import Database

from specifai.general.backend.utils.test_utils import random_lower_string
from specifai.items.backend.data_models.item_models import Item, ItemCreate
from specifai.items.backend.data_repository.item_data_repository_mongo import (
    MongoItemDataRepository,
)
from specifai.users.backend.components.user_test_utils import create_random_user
from specifai.workspaces.backend.data_repository.workspace_data_repository_mongo import (
    MongoWorkspaceDataRepository,
)


def create_random_item(db: Database[dict[str, Any]]) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    workspace_repo = MongoWorkspaceDataRepository(db)
    workspace = workspace_repo.get_or_create_default_workspace(owner_id=owner_id)
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(
        title=title, description=description, workspace_id=workspace.id
    )
    repo = MongoItemDataRepository(db)
    return repo.create_item(
        item_in=item_in, owner_id=owner_id, workspace_id=workspace.id
    )
