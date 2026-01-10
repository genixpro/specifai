import uuid
from unittest.mock import MagicMock

from specifai.general.backend.components import db as db_module


def test_init_db_creates_superuser_and_workspace(monkeypatch) -> None:
    session = MagicMock()
    user_repo = MagicMock()
    workspace_repo = MagicMock()
    user = MagicMock()
    user.id = uuid.uuid4()
    user_repo.get_user_by_email.return_value = None
    user_repo.create_user.return_value = user

    monkeypatch.setattr(db_module, "PostgresUserDataRepository", lambda _: user_repo)
    monkeypatch.setattr(
        db_module, "PostgresWorkspaceDataRepository", lambda _: workspace_repo
    )
    monkeypatch.setattr(db_module.settings, "FIRST_SUPERUSER", "admin@example.com")
    monkeypatch.setattr(db_module.settings, "FIRST_SUPERUSER_PASSWORD", "supersecret")

    db_module.init_db(session)

    user_repo.get_user_by_email.assert_called_once_with("admin@example.com")
    assert user_repo.create_user.call_count == 1
    user_create = user_repo.create_user.call_args.kwargs["user_create"]
    assert user_create.email == "admin@example.com"
    assert user_create.is_superuser is True
    workspace_repo.get_or_create_default_workspace.assert_called_once_with(
        owner_id=user.id
    )


def test_init_db_uses_existing_superuser(monkeypatch) -> None:
    session = MagicMock()
    user_repo = MagicMock()
    workspace_repo = MagicMock()
    user = MagicMock()
    user.id = uuid.uuid4()
    user_repo.get_user_by_email.return_value = user

    monkeypatch.setattr(db_module, "PostgresUserDataRepository", lambda _: user_repo)
    monkeypatch.setattr(
        db_module, "PostgresWorkspaceDataRepository", lambda _: workspace_repo
    )
    monkeypatch.setattr(db_module.settings, "FIRST_SUPERUSER", "admin@example.com")

    db_module.init_db(session)

    user_repo.get_user_by_email.assert_called_once_with("admin@example.com")
    user_repo.create_user.assert_not_called()
    workspace_repo.get_or_create_default_workspace.assert_called_once_with(
        owner_id=user.id
    )
