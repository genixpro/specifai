from specifai.general.backend.components.security import verify_password
from specifai.users.backend.data_repository.user_data_repository_base import (
    UserDataRepository,
)
from specifai.users.backend.data_models.user_models import User


def authenticate(
    *, repo: UserDataRepository, email: str, password: str
) -> User | None:
    db_user = repo.get_user_by_email(email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
