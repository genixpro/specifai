from unittest.mock import MagicMock

import pytest

from specifai.users.backend.data_repository.user_data_repository_base import (
    UserDataRepository,
)


class DummyUserRepository(UserDataRepository):
    def get_user_by_id(self, user_id):
        return super().get_user_by_id(user_id)

    def get_user_by_email(self, email):
        return super().get_user_by_email(email)

    def list_users(self, *, skip, limit):
        return super().list_users(skip=skip, limit=limit)

    def create_user(self, *, user_create):
        return super().create_user(user_create=user_create)

    def create_user_with_hashed_password(self, *, email, full_name, hashed_password):
        return super().create_user_with_hashed_password(
            email=email, full_name=full_name, hashed_password=hashed_password
        )

    def update_user_from_update(self, *, db_user, user_in):
        return super().update_user_from_update(db_user=db_user, user_in=user_in)

    def update_user_fields(self, *, db_user, user_data, extra_data=None):
        return super().update_user_fields(
            db_user=db_user, user_data=user_data, extra_data=extra_data
        )

    def update_user_me(self, *, db_user, user_in):
        return super().update_user_me(db_user=db_user, user_in=user_in)

    def set_user_password(self, *, db_user, hashed_password):
        return super().set_user_password(
            db_user=db_user, hashed_password=hashed_password
        )

    def delete_user(self, *, db_user):
        return super().delete_user(db_user=db_user)


def test_user_data_repository_base_raises_not_implemented() -> None:
    repo = DummyUserRepository()
    with pytest.raises(NotImplementedError):
        repo.get_user_by_id(None)
    with pytest.raises(NotImplementedError):
        repo.get_user_by_email("user@example.com")
    with pytest.raises(NotImplementedError):
        repo.list_users(skip=0, limit=1)
    with pytest.raises(NotImplementedError):
        repo.create_user(user_create=MagicMock())
    with pytest.raises(NotImplementedError):
        repo.create_user_with_hashed_password(
            email="user@example.com", full_name=None, hashed_password="hash"
        )
    with pytest.raises(NotImplementedError):
        repo.update_user_from_update(db_user=MagicMock(), user_in=MagicMock())
    with pytest.raises(NotImplementedError):
        repo.update_user_fields(db_user=MagicMock(), user_data={}, extra_data=None)
    with pytest.raises(NotImplementedError):
        repo.update_user_me(db_user=MagicMock(), user_in=MagicMock())
    with pytest.raises(NotImplementedError):
        repo.set_user_password(db_user=MagicMock(), hashed_password="hash")
    with pytest.raises(NotImplementedError):
        repo.delete_user(db_user=MagicMock())
