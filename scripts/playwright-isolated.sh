#! /usr/bin/env bash

set -euo pipefail

compose_file="docker-compose.playwright-isolated.yml"

mkdir -p ./test-results
mkdir -p ./specifai/general/frontend/blob-report
mkdir -p ./playwright-report

docker compose -f "$compose_file" down -v --remove-orphans
docker compose -f "$compose_file" build
docker compose -f "$compose_file" up -d pw-db pw-mailcatcher pw-prestart pw-backend pw-frontend
docker compose -f "$compose_file" run --rm pw-playwright "$@"
docker compose -f "$compose_file" down -v --remove-orphans
