from datetime import timedelta

import jwt

from specifai.general.backend.components.config import settings
from specifai.general.backend.components.security import (
    ALGORITHM,
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_create_access_token_contains_subject(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SECRET_KEY", "test-secret")
    token = create_access_token("user-123", timedelta(minutes=5))
    decoded = jwt.decode(token, "test-secret", algorithms=[ALGORITHM])
    assert decoded["sub"] == "user-123"
    assert "exp" in decoded


def test_password_helpers_round_trip() -> None:
    password = "a-secure-password"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong-password", hashed_password) is False
