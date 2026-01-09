from collections.abc import Generator
from typing import Annotated
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from specifai.auth.backend.data_models.auth_models import TokenPayload
from specifai.general.backend.components import security
from specifai.general.backend.components.config import settings
from specifai.general.backend.components.db import engine
from specifai.items.backend.data_repository.item_data_repository_base import (
    ItemDataRepository,
)
from specifai.items.backend.data_repository.item_data_repository_postgres import (
    PostgresItemDataRepository,
)
from specifai.users.backend.data_repository.user_data_repository_base import (
    UserDataRepository,
)
from specifai.users.backend.data_repository.user_data_repository_postgres import (
    PostgresUserDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_base import (
    WorkspaceDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)
from specifai.users.backend.data_models.user_models import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_user_repository(session: SessionDep) -> UserDataRepository:
    return PostgresUserDataRepository(session)


def get_item_repository(session: SessionDep) -> ItemDataRepository:
    return PostgresItemDataRepository(session)


def get_workspace_repository(session: SessionDep) -> WorkspaceDataRepository:
    return PostgresWorkspaceDataRepository(session)


UserRepoDep = Annotated[UserDataRepository, Depends(get_user_repository)]
ItemRepoDep = Annotated[ItemDataRepository, Depends(get_item_repository)]
WorkspaceRepoDep = Annotated[
    WorkspaceDataRepository, Depends(get_workspace_repository)
]


def get_current_user(repo: UserRepoDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user_id = uuid.UUID(token_data.sub) if token_data.sub else None
    user = repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
