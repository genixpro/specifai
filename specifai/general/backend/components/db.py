from sqlmodel import Session, create_engine

from specifai.general.backend.components.config import settings
from specifai.users.backend.data_repository.user_data_repository_postgres import (
    PostgresUserDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)
from specifai.items.backend.data_models import item_models  # noqa: F401
from specifai.users.backend.data_models import user_models  # noqa: F401
from specifai.users.backend.data_models.user_models import UserCreate
from specifai.workspaces.backend.data_models import workspace_models  # noqa: F401

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user_repo = PostgresUserDataRepository(session)
    workspace_repo = PostgresWorkspaceDataRepository(session)
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
