from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from bradstarter.general.backend.apis.deps import SessionDep
from bradstarter.general.backend.components.security import get_password_hash
from bradstarter.users.backend.data_models.user_models import User, UserPublic

router = APIRouter(tags=["private"], prefix="/private")


class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False


@router.post("/users/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user.
    """

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
    )

    session.add(user)
    session.commit()

    return user
