#! /usr/bin/env bash

set -euo pipefail

until curl -sf http://pw-backend:8000/api/v1/utils/health-check/ > /dev/null; do
  sleep 1
done

until curl -sf http://pw-frontend > /dev/null; do
  sleep 1
done

if [ "$#" -eq 0 ]; then
  exec npx playwright test
fi

exec npx playwright test "$@"
