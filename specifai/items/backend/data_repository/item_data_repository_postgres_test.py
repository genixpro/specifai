from pymongo.database import Database

from specifai.general.backend.utils.test_utils import random_email, random_lower_string
from specifai.items.backend.data_models.item_models import ItemCreate
from specifai.items.backend.data_repository.item_data_repository_mongo import (
    MongoItemDataRepository,
)
from specifai.users.backend.data_models.user_models import UserCreate
from specifai.users.backend.data_repository.user_data_repository_mongo import (
    MongoUserDataRepository,
)
from specifai.workspaces.backend.data_models.workspace_models import WorkspaceCreate
from specifai.workspaces.backend.data_repository.workspace_data_repository_mongo import (
    MongoWorkspaceDataRepository,
)


def test_item_repository_crud(db: Database) -> None:
    user_repo = MongoUserDataRepository(db)
    workspace_repo = MongoWorkspaceDataRepository(db)
    item_repo = MongoItemDataRepository(db)

    user = user_repo.create_user(
        user_create=UserCreate(email=random_email(), password=random_lower_string())
    )
    workspace = workspace_repo.create_workspace(
        workspace_in=WorkspaceCreate(name=random_lower_string()), owner_id=user.id
    )

    title = random_lower_string()
    item = item_repo.create_item(
        item_in=ItemCreate(
            title=title, description=random_lower_string(), workspace_id=workspace.id
        ),
        owner_id=user.id,
        workspace_id=workspace.id,
    )
    assert item.id

    fetched = item_repo.get_item_by_id(item.id)
    assert fetched
    assert fetched.title == title

    items, count = item_repo.list_items(
        owner_id=user.id, workspace_id=None, skip=0, limit=100
    )
    assert count >= 1
    assert any(db_item.id == item.id for db_item in items)

    updated = item_repo.update_item(item=item, update_data={"title": "Updated"})
    assert updated.title == "Updated"

    item_repo.delete_item(item=updated)
    assert item_repo.get_item_by_id(updated.id) is None


def test_item_repository_delete_by_user(db: Database) -> None:
    user_repo = MongoUserDataRepository(db)
    workspace_repo = MongoWorkspaceDataRepository(db)
    item_repo = MongoItemDataRepository(db)

    user = user_repo.create_user(
        user_create=UserCreate(email=random_email(), password=random_lower_string())
    )
    workspace = workspace_repo.create_workspace(
        workspace_in=WorkspaceCreate(name=random_lower_string()), owner_id=user.id
    )

    for _ in range(2):
        item_repo.create_item(
            item_in=ItemCreate(
                title=random_lower_string(),
                description=random_lower_string(),
                workspace_id=workspace.id,
            ),
            owner_id=user.id,
            workspace_id=workspace.id,
        )

    item_repo.delete_items_for_user(user_id=user.id)
    _items, count = item_repo.list_items(
        owner_id=user.id, workspace_id=None, skip=0, limit=100
    )
    assert count == 0
