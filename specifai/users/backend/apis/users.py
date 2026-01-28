import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from specifai.general.backend.apis.deps import (
    CurrentUser,
    ItemRepoDep,
    UserRepoDep,
    WorkspaceRepoDep,
    get_current_active_superuser,
)
from specifai.general.backend.components.config import settings
from specifai.general.backend.components.security import (
    get_password_hash,
    verify_password,
)
from specifai.general.backend.data_models.message_models import Message
from specifai.general.backend.utils.utils import generate_new_account_email, send_email
from specifai.users.backend.data_models.user_models import (
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(repo: UserRepoDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    users, count = repo.list_users(skip=skip, limit=limit)
    return UsersPublic(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(
    *,
    user_repo: UserRepoDep,
    workspace_repo: WorkspaceRepoDep,
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = user_repo.get_user_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = user_repo.create_user(user_create=user_in)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, user_repo: UserRepoDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = user_repo.get_user_by_email(user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    return user_repo.update_user_me(db_user=current_user, user_in=user_in)


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, user_repo: UserRepoDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    user_repo.set_user_password(db_user=current_user, hashed_password=hashed_password)
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(user_repo: UserRepoDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    user_repo.delete_user(db_user=current_user)
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(
    user_repo: UserRepoDep, workspace_repo: WorkspaceRepoDep, user_in: UserRegister
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = user_repo.get_user_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate(**user_in.model_dump())
    user = user_repo.create_user(user_create=user_create)
    workspace_repo.get_or_create_default_workspace(owner_id=user.id)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, repo: UserRepoDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = repo.get_user_by_id(user_id)
    if user and user.id == current_user.id:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    repo: UserRepoDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = repo.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = repo.get_user_by_email(user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = repo.update_user_from_update(db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    user_repo: UserRepoDep,
    item_repo: ItemRepoDep,
    current_user: CurrentUser,
    user_id: uuid.UUID,
) -> Message:
    """
    Delete a user.
    """
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    item_repo.delete_items_for_user(user_id=user_id)
    user_repo.delete_user(db_user=user)
    return Message(message="User deleted successfully")
