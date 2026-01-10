from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from specifai.auth.backend.components.auth_service import authenticate
from specifai.general.backend.components.security import verify_password
from specifai.general.backend.utils.test_utils import (
    random_email,
    random_lower_string,
)
from specifai.users.backend.data_models.user_models import UserCreate, UserUpdate
from specifai.users.backend.data_repository.user_data_repository_postgres import (
    PostgresUserDataRepository,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_postgres import (
    PostgresWorkspaceDataRepository,
)


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    authenticated_user = authenticate(repo=repo, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    repo = PostgresUserDataRepository(db)
    user = authenticate(repo=repo, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert user.is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, disabled=True)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert user.is_active


def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert user.is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    assert user.is_superuser is False


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    repo = PostgresUserDataRepository(db)
    user_2 = repo.get_user_by_id(user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    repo = PostgresUserDataRepository(db)
    workspace_repo = PostgresWorkspaceDataRepository(db)
    user = repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    if user.id is not None:
        repo.update_user_from_update(db_user=user, user_in=user_in_update)
    user_2 = repo.get_user_by_id(user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
