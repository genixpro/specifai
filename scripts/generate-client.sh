#! /usr/bin/env bash

set -e
set -x

python -c "import json; from bradstarter.general.backend.components.main import app; print(json.dumps(app.openapi()))" > bradstarter/general/frontend/openapi.json
npm run generate-client
