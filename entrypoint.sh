#!/bin/sh
set -e

RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

cd /code

# gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT src.main:app
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
