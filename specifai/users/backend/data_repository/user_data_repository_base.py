from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any

from specifai.users.backend.data_models.user_models import (
    User,
    UserCreate,
    UserUpdate,
    UserUpdateMe,
)


class UserDataRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: uuid.UUID | None) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def list_users(self, *, skip: int, limit: int) -> tuple[list[User], int]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, *, user_create: UserCreate) -> User:
        raise NotImplementedError

    @abstractmethod
    def create_user_with_hashed_password(
        self, *, email: str, full_name: str | None, hashed_password: str
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def update_user_from_update(self, *, db_user: User, user_in: UserUpdate) -> User:
        raise NotImplementedError

    @abstractmethod
    def update_user_fields(
        self,
        *,
        db_user: User,
        user_data: dict[str, Any],
        extra_data: dict[str, Any] | None = None,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def update_user_me(self, *, db_user: User, user_in: UserUpdateMe) -> User:
        raise NotImplementedError

    @abstractmethod
    def set_user_password(self, *, db_user: User, hashed_password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, *, db_user: User) -> None:
        raise NotImplementedError
