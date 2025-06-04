#!/bin/sh
set -e

RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

cd /code
# Only apply existing migrations, don't create new ones
echo "Running database migrations..."
alembic upgrade head

cd /code/src
# Start the application
echo "Starting application..."
uvicorn main:app --host ${RUN_HOST} --port ${RUN_PORT} --reload
