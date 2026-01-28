from typing import Any

from pymongo.database import Database

from specifai.general.backend.components.security import (
    get_password_hash,
    verify_password,
)
from specifai.general.backend.utils.test_utils import random_email, random_lower_string
from specifai.users.backend.data_models.user_models import (
    UserCreate,
    UserUpdate,
    UserUpdateMe,
)
from specifai.users.backend.data_repository.user_data_repository_mongo import (
    MongoUserDataRepository,
)


def test_user_repository_crud(db: Database[dict[str, Any]]) -> None:
    repo = MongoUserDataRepository(db)
    email = random_email()
    password = random_lower_string()

    user = repo.create_user(user_create=UserCreate(email=email, password=password))
    assert user.id

    fetched = repo.get_user_by_email(email)
    assert fetched
    assert fetched.id == user.id

    users, count = repo.list_users(skip=0, limit=1000)
    assert count >= 1
    assert any(db_user.id == user.id for db_user in users)

    updated = repo.update_user_from_update(
        db_user=user, user_in=UserUpdate(full_name="Repo Test User")
    )
    assert updated.full_name == "Repo Test User"

    new_password = random_lower_string()
    updated_pw = repo.update_user_from_update(
        db_user=updated, user_in=UserUpdate(password=new_password)
    )
    assert verify_password(new_password, updated_pw.hashed_password)

    repo.delete_user(db_user=updated_pw)
    assert repo.get_user_by_id(updated_pw.id) is None


def test_user_repository_password_helpers(db: Database[dict[str, Any]]) -> None:
    repo = MongoUserDataRepository(db)
    email = random_email()
    raw_password = random_lower_string()
    hashed_password = get_password_hash(raw_password)

    user = repo.create_user_with_hashed_password(
        email=email, full_name="Hashed User", hashed_password=hashed_password
    )
    assert verify_password(raw_password, user.hashed_password)

    next_password = random_lower_string()
    repo.set_user_password(
        db_user=user, hashed_password=get_password_hash(next_password)
    )
    refreshed = repo.get_user_by_id(user.id)
    assert refreshed
    assert verify_password(next_password, refreshed.hashed_password)


def test_user_repository_update_helpers(db: Database[dict[str, Any]]) -> None:
    repo = MongoUserDataRepository(db)
    user = repo.create_user(
        user_create=UserCreate(email=random_email(), password=random_lower_string())
    )
    updated = repo.update_user_fields(
        db_user=user, user_data={"full_name": "Updated"}, extra_data=None
    )
    assert updated.full_name == "Updated"

    updated_me = repo.update_user_me(
        db_user=updated, user_in=UserUpdateMe(full_name="Updated Me")
    )
    assert updated_me.full_name == "Updated Me"


def test_user_repository_none_id_short_circuit(db: Database[dict[str, Any]]) -> None:
    repo = MongoUserDataRepository(db)
    assert repo.get_user_by_id(None) is None
