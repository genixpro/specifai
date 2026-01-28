import warnings

import pytest

from specifai.general.backend.components.config import Settings, parse_cors


def _base_settings_kwargs() -> dict[str, object]:
    return {
        "PROJECT_NAME": "Specifai",
        "MONGODB_SERVER": "db.local",
        "MONGODB_DB": "specifai",
        "FIRST_SUPERUSER": "admin@example.com",
        "FIRST_SUPERUSER_PASSWORD": "supersecret",
        "EMAILS_FROM_EMAIL": "no-reply@example.com",
    }


def test_parse_cors_string_to_list() -> None:
    parsed = parse_cors("https://a.com, https://b.com")
    assert parsed == ["https://a.com", "https://b.com"]


def test_parse_cors_list_passthrough() -> None:
    parsed = parse_cors(["https://a.com"])
    assert parsed == ["https://a.com"]


def test_parse_cors_json_string_passthrough() -> None:
    parsed = parse_cors('["https://a.com"]')
    assert parsed == '["https://a.com"]'


def test_parse_cors_invalid_raises() -> None:
    with pytest.raises(ValueError):
        parse_cors(123)


def test_settings_all_cors_origins_and_mailcatcher_defaults() -> None:
    settings = Settings(
        **_base_settings_kwargs(),
        BACKEND_CORS_ORIGINS="https://a.com/, https://b.com",
        MAILCATCHER_HOST="mailcatcher",
        ENVIRONMENT="local",
    )
    assert [str(origin) for origin in settings.BACKEND_CORS_ORIGINS] == [
        "https://a.com/",
        "https://b.com/",
    ]
    assert settings.all_cors_origins == [
        "https://a.com",
        "https://b.com",
        settings.FRONTEND_HOST,
    ]
    assert settings.EMAILS_FROM_NAME == "Specifai"
    assert settings.SMTP_HOST == "mailcatcher"
    assert settings.SMTP_PORT == 1025
    assert settings.emails_enabled is True


def test_settings_mongodb_uri() -> None:
    base_kwargs = _base_settings_kwargs()
    base_kwargs["MONGODB_SERVER"] = "db.internal"
    settings = Settings(
        **base_kwargs,
        MONGODB_PORT=27019,
        MONGODB_USER="mongo",
        MONGODB_PASSWORD="password",
    )
    assert (
        settings.mongo_uri
        == "mongodb://mongo:password@db.internal:27019/specifai?authSource=admin"
    )


def test_settings_default_secret_warns_in_local() -> None:
    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        base_kwargs = _base_settings_kwargs()
        base_kwargs["FIRST_SUPERUSER_PASSWORD"] = "changethis"
        Settings(
            **base_kwargs,
            SECRET_KEY="changethis",
            MONGODB_PASSWORD="changethis",
            ENVIRONMENT="local",
        )
        warning_messages = [
            str(warning.message)
            for warning in warning_list
            if "changethis" in str(warning.message)
        ]
        assert len(warning_messages) == 3


def test_settings_default_secret_rejected_in_production() -> None:
    with pytest.raises(ValueError):
        Settings(
            **_base_settings_kwargs(),
            SECRET_KEY="changethis",
            ENVIRONMENT="production",
        )
