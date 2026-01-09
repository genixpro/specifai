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

if command -v coverage >/dev/null 2>&1; then
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
    "$PYTEST_BIN" .
fi
