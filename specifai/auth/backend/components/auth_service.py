from sqlmodel import Session

from specifai.general.backend.components.security import verify_password
from specifai.users.backend.components.user_crud import get_user_by_email
from specifai.users.backend.data_models.user_models import User


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
