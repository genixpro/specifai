#! /usr/bin/env bash

set -e
set -x

python -c "import json; from specifai.general.backend.components.main import app; print(json.dumps(app.openapi()))" > specifai/general/frontend/openapi.json
npm run generate-client
