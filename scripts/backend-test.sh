#!/usr/bin/env bash

set -e
set -x

PYTHON_BIN="python3"
PYTEST_BIN="pytest"
if [ -x "venv/bin/python" ]; then
    PYTHON_BIN="venv/bin/python"
fi
if [ -x "venv/bin/pytest" ]; then
    PYTEST_BIN="venv/bin/pytest"
fi

HAS_PYTEST_COV=0
if "$PYTHON_BIN" - <<'PY'
try:
    import pytest_cov  # noqa: F401
except Exception:
    raise SystemExit(1)
PY
then
    HAS_PYTEST_COV=1
fi

HAS_XDIST=0
if "$PYTHON_BIN" - <<'PY'
try:
    import xdist  # noqa: F401
except Exception:
    raise SystemExit(1)
PY
then
    HAS_XDIST=1
fi

PYTEST_ARGS=()
USE_XDIST=0
if [ "$HAS_XDIST" -eq 1 ]; then
    USE_XDIST=1
fi
if [ -n "${PYTEST_XDIST_DISABLE:-}" ]; then
    USE_XDIST=0
fi
if [ "$USE_XDIST" -eq 1 ]; then
    PYTEST_ARGS+=("-n" "auto")
fi

if [ "$HAS_PYTEST_COV" -eq 1 ]; then
    "$PYTEST_BIN" "${PYTEST_ARGS[@]}" --cov=specifai --cov-report=term --cov-report=html --cov-context=test .
elif command -v coverage >/dev/null 2>&1; then
    coverage run -m pytest .
    coverage report
    coverage html --title "${@-coverage}"
elif "$PYTHON_BIN" - <<'PY'
try:
    import coverage  # noqa: F401
except Exception:
    raise SystemExit(1)
PY
then
    "$PYTHON_BIN" -m coverage run -m pytest .
    "$PYTHON_BIN" -m coverage report
    "$PYTHON_BIN" -m coverage html --title "${@-coverage}"
else
    "$PYTEST_BIN" "${PYTEST_ARGS[@]}" .
fi
