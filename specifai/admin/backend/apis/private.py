from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from specifai.general.backend.apis.deps import UserRepoDep
from specifai.general.backend.components.security import get_password_hash
from specifai.users.backend.data_models.user_models import UserPublic

router = APIRouter(tags=["private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False


@router.post("/users/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, repo: UserRepoDep) -> Any:
    """
    Create a new user.
    """

    return repo.create_user_with_hashed_password(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )
