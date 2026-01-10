from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import select

from specifai.general.backend.components.tests_pre_start import init, logger


def test_init_successful_connection() -> None:
    engine_mock = MagicMock()

    session_mock = MagicMock()
    exec_mock = MagicMock(return_value=True)
    session_mock.configure_mock(**{"exec.return_value": exec_mock})

    with (
        patch("sqlmodel.Session", return_value=session_mock),
        patch.object(logger, "info"),
        patch.object(logger, "error"),
        patch.object(logger, "warn"),
    ):
        try:
            init(engine_mock)
            connection_successful = True
        except Exception:
            connection_successful = False

        assert (
            connection_successful
        ), "The database connection should be successful and not raise an exception."

        assert session_mock.exec.called_once_with(
            select(1)
        ), "The session should execute a select statement once."


def test_init_failure_logs_and_raises() -> None:
    engine_mock = MagicMock()
    session_mock = MagicMock()
    session_mock.exec.side_effect = RuntimeError("db down")
    session_context = MagicMock()
    session_context.__enter__.return_value = session_mock
    session_context.__exit__.return_value = None

    with (
        patch(
            "specifai.general.backend.components.tests_pre_start.Session",
            return_value=session_context,
        ),
        patch.object(logger, "error") as logger_error,
    ):
        with pytest.raises(RuntimeError, match="db down"):
            init(engine_mock)
        logger_error.assert_called_once()


def test_main_calls_init() -> None:
    with (
        patch("specifai.general.backend.components.tests_pre_start.init") as init_mock,
        patch.object(logger, "info"),
    ):
        from specifai.general.backend.components import tests_pre_start

        tests_pre_start.main()
        init_mock.assert_called_once()
