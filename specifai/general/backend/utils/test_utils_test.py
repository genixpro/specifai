from unittest.mock import MagicMock

from specifai.general.backend.components.config import settings
from specifai.general.backend.utils import test_utils


def test_random_lower_string_is_lowercase() -> None:
    value = test_utils.random_lower_string()
    assert len(value) == 32
    assert value.islower()


def test_random_email_format() -> None:
    email = test_utils.random_email()
    assert "@" in email
    assert email.endswith(".com")


def test_get_superuser_token_headers(monkeypatch) -> None:
    monkeypatch.setattr(settings, "FIRST_SUPERUSER", "admin@example.com")
    monkeypatch.setattr(settings, "FIRST_SUPERUSER_PASSWORD", "supersecret")
    monkeypatch.setattr(settings, "API_V1_STR", "/api/v1")

    client = MagicMock()
    response = MagicMock()
    response.json.return_value = {"access_token": "token"}
    client.post.return_value = response

    headers = test_utils.get_superuser_token_headers(client)

    client.post.assert_called_once_with(
        "/api/v1/login/access-token",
        data={"username": "admin@example.com", "password": "supersecret"},
    )
    assert headers == {"Authorization": "Bearer token"}
