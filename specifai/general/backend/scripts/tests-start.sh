#! /usr/bin/env bash
set -e
set -x

python -m specifai.general.backend.components.tests_pre_start

bash specifai/general/backend/scripts/test.sh "$@"
