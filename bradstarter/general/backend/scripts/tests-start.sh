#! /usr/bin/env bash
set -e
set -x

python -m bradstarter.general.backend.components.tests_pre_start

bash bradstarter/general/backend/scripts/test.sh "$@"
