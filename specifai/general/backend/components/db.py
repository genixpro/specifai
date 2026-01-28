from pymongo import MongoClient
from pymongo.database import Database

from specifai.general.backend.components.config import settings
from specifai.users.backend.data_models.user_models import UserCreate
from specifai.users.backend.data_repository.user_data_repository_mongo import (
    MongoUserDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_mongo import (
    MongoWorkspaceDataRepository,
)

mongo_client = MongoClient(settings.mongo_uri)
mongo_db = mongo_client[settings.MONGODB_DB]


def get_database() -> Database:
    return mongo_db


def close_database() -> None:
    mongo_client.close()


def init_db(db: Database) -> None:
    _ensure_indexes(db)
    user_repo = MongoUserDataRepository(db)
    workspace_repo = MongoWorkspaceDataRepository(db)
    user = user_repo.get_user_by_email(settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = user_repo.create_user(user_create=user_in)
    if user:
        workspace_repo.get_or_create_default_workspace(owner_id=user.id)


def _ensure_indexes(db: Database) -> None:
    db["users"].create_index("email", unique=True)
    db["items"].create_index([("owner_id", 1), ("workspace_id", 1)])
    db["workspaces"].create_index([("owner_id", 1), ("name", 1)])
