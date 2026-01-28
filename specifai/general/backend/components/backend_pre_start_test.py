from unittest.mock import MagicMock, patch

import pytest

from specifai.general.backend.components.backend_pre_start import init, logger


def test_init_successful_connection() -> None:
    db_mock = MagicMock()
    db_mock.command.return_value = {"ok": 1}

    with (
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(db_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

        assert (
            connection_successful
        ), "The database connection should be successful and not raise an exception."

        db_mock.command.assert_called_once_with("ping")


def test_init_failure_logs_and_raises() -> None:
    db_mock = MagicMock()
    db_mock.command.side_effect = RuntimeError("db down")

    with (
        patch.object(logger, "error") as logger_error,
    ):
        with pytest.raises(RuntimeError, match="db down"):
            init(db_mock)
        logger_error.assert_called_once()


def test_main_calls_init() -> None:
    with (
        patch(
            "specifai.general.backend.components.backend_pre_start.init"
        ) as init_mock,
        patch.object(logger, "info"),
    ):
        from specifai.general.backend.components import backend_pre_start

        backend_pre_start.main()
        init_mock.assert_called_once()
