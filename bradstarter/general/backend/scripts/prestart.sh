#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python -m bradstarter.general.backend.components.backend_pre_start

# Run migrations
alembic upgrade head

# Create initial data in DB
python -m bradstarter.general.backend.components.initial_data
