from __future__ import annotations

import uuid
from collections.abc import Iterable
from typing import Any

from pymongo.database import Database

from specifai.general.backend.components.security import get_password_hash
from specifai.users.backend.data_models.user_models import (
    User,
    UserCreate,
    UserUpdate,
    UserUpdateMe,
)
from specifai.users.backend.data_repository.user_data_repository_base import (
    UserDataRepository,
)


class MongoUserDataRepository(UserDataRepository):
    def __init__(self, db: Database[dict[str, Any]]) -> None:
        self._db = db
        self._collection = db["users"]

    def get_user_by_id(self, user_id: uuid.UUID | None) -> User | None:
        if user_id is None:
            return None
        doc = self._collection.find_one({"_id": str(user_id)})
        return self._doc_to_user(doc)

    def get_user_by_email(self, email: str) -> User | None:
        doc = self._collection.find_one({"email": email})
        return self._doc_to_user(doc)

    def list_users(self, *, skip: int, limit: int) -> tuple[list[User], int]:
        count = self._collection.count_documents({})
        cursor = self._collection.find({}).skip(skip).limit(limit)
        return self._cursor_to_users(cursor), count

    def create_user(self, *, user_create: UserCreate) -> User:
        user_data = user_create.model_dump(exclude={"password"})
        user = User(
            **user_data,
            hashed_password=get_password_hash(user_create.password),
        )
        self._collection.insert_one(self._user_to_doc(user))
        return user

    def create_user_with_hashed_password(
        self, *, email: str, full_name: str | None, hashed_password: str
    ) -> User:
        user = User(email=email, full_name=full_name, hashed_password=hashed_password)
        self._collection.insert_one(self._user_to_doc(user))
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
        update_payload = {**user_data, **extra_data}
        update_payload.pop("password", None)
        if not update_payload:
            return db_user
        self._collection.update_one(
            {"_id": str(db_user.id)},
            {"$set": self._serialize_user_update(update_payload)},
        )
        refreshed = self.get_user_by_id(db_user.id)
        if refreshed is None:
            raise ValueError("User not found after update")
        return refreshed

    def update_user_me(self, *, db_user: User, user_in: UserUpdateMe) -> User:
        user_data = user_in.model_dump(exclude_unset=True)
        return self.update_user_fields(db_user=db_user, user_data=user_data)

    def set_user_password(self, *, db_user: User, hashed_password: str) -> User:
        self._collection.update_one(
            {"_id": str(db_user.id)}, {"$set": {"hashed_password": hashed_password}}
        )
        refreshed = self.get_user_by_id(db_user.id)
        if refreshed is None:
            raise ValueError("User not found after password update")
        return refreshed

    def delete_user(self, *, db_user: User) -> None:
        self._collection.delete_one({"_id": str(db_user.id)})
        self._db["items"].delete_many({"owner_id": str(db_user.id)})
        self._db["workspaces"].delete_many({"owner_id": str(db_user.id)})

    def _serialize_user_update(self, update_payload: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for key, value in update_payload.items():
            if value is None:
                payload[key] = None
            elif isinstance(value, uuid.UUID):
                payload[key] = str(value)
            else:
                payload[key] = value
        return payload

    def _user_to_doc(self, user: User) -> dict[str, Any]:
        data = user.model_dump()
        data["_id"] = str(data.pop("id"))
        return self._serialize_user_update(data)

    def _doc_to_user(self, doc: dict[str, Any] | None) -> User | None:
        if not doc:
            return None
        data = dict(doc)
        data["id"] = uuid.UUID(str(data.pop("_id")))
        return User.model_validate(data)

    def _cursor_to_users(self, cursor: Iterable[dict[str, Any]]) -> list[User]:
        users: list[User] = []
        for doc in cursor:
            user = self._doc_to_user(doc)
            if user:
                users.append(user)
        return users
