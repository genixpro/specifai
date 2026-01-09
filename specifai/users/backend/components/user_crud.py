from typing import Any

from sqlmodel import Session

from specifai.users.backend.data_repository.user_data_repository_postgres import (
    PostgresUserDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)
from specifai.users.backend.data_models.user_models import (
    User,
    UserCreate,
    UserUpdate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    user_repo = PostgresUserDataRepository(session)
    workspace_repo = PostgresWorkspaceDataRepository(session)
    user = user_repo.create_user(user_create=user_create)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    return user


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    repo = PostgresUserDataRepository(session)
    return repo.update_user_from_update(db_user=db_user, user_in=user_in)


def get_user_by_email(*, session: Session, email: str) -> User | None:
    repo = PostgresUserDataRepository(session)
    return repo.get_user_by_email(email)
