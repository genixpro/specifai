from __future__ import annotations

from typing import Any
import uuid

from sqlmodel import Session, func, select

from specifai.general.backend.components.security import get_password_hash
from specifai.users.backend.data_repository.user_data_repository_base import (
    UserDataRepository,
)
from specifai.users.backend.data_models.user_models import (
    User,
    UserCreate,
    UserUpdate,
    UserUpdateMe,
)


class PostgresUserDataRepository(UserDataRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_user_by_id(self, user_id: uuid.UUID | None) -> User | None:
        if user_id is None:
            return None
        self._session.expire_all()
        return self._session.get(User, user_id)

    def get_user_by_email(self, email: str) -> User | None:
        self._session.expire_all()
        statement = select(User).where(User.email == email)
        return self._session.exec(statement).first()

    def list_users(self, *, skip: int, limit: int) -> tuple[list[User], int]:
        self._session.expire_all()
        count_statement = select(func.count()).select_from(User)
        count = self._session.exec(count_statement).one()
        statement = select(User).offset(skip).limit(limit)
        users = self._session.exec(statement).all()
        return list(users), count

    def create_user(self, *, user_create: UserCreate) -> User:
        db_obj = User.model_validate(
            user_create,
            update={"hashed_password": get_password_hash(user_create.password)},
        )
        self._session.add(db_obj)
        self._session.commit()
        self._session.refresh(db_obj)
        return db_obj

    def create_user_with_hashed_password(
        self, *, email: str, full_name: str | None, hashed_password: str
    ) -> User:
        user = User(email=email, full_name=full_name, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def update_user_from_update(self, *, db_user: User, user_in: UserUpdate) -> User:
        user_data = user_in.model_dump(exclude_unset=True)
        extra_data: dict[str, Any] = {}
        if "password" in user_data:
            hashed_password = get_password_hash(user_data["password"])
            extra_data["hashed_password"] = hashed_password
        return self.update_user_fields(
            db_user=db_user, user_data=user_data, extra_data=extra_data
        )

    def update_user_fields(
        self,
        *,
        db_user: User,
        user_data: dict[str, Any],
        extra_data: dict[str, Any] | None = None,
    ) -> User:
        if extra_data is None:
            extra_data = {}
        db_user.sqlmodel_update(user_data, update=extra_data)
        self._session.add(db_user)
        self._session.commit()
        self._session.refresh(db_user)
        return db_user

    def update_user_me(self, *, db_user: User, user_in: UserUpdateMe) -> User:
        user_data = user_in.model_dump(exclude_unset=True)
        return self.update_user_fields(db_user=db_user, user_data=user_data)

    def set_user_password(self, *, db_user: User, hashed_password: str) -> User:
        db_user.hashed_password = hashed_password
        self._session.add(db_user)
        self._session.commit()
        self._session.refresh(db_user)
        return db_user

    def delete_user(self, *, db_user: User) -> None:
        self._session.delete(db_user)
        self._session.commit()
