#!/bin/sh
set -e

RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

cd /code

# Run database migrations
echo "Running database migrations..."
# Check if Aerich is initialized
if [ ! -d "migrations" ]; then
  echo "Initializing Aerich..."
  aerich init -t core.db.TORTOISE_ORM
fi

# Check if database is initialized
if ! aerich history | grep -q "No history"; then
  echo "Upgrading database..."
  aerich upgrade
else
  echo "Initializing database..."
  aerich init-db
fi

# Start the application
echo "Starting application..."
# gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT src.main:app
uvicorn main:app --host ${RUN_HOST} --port ${RUN_PORT} --reload
