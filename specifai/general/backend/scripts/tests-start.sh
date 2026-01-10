#! /usr/bin/env bash
set -e
set -x

python -m specifai.general.backend.components.tests_pre_start

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${script_dir}/test.sh" "$@"
