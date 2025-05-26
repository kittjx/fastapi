#!/bin/sh
set -e

RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

cd /code

# gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT src.main:app
uvicorn main:app --host ${RUN_HOST} --port ${RUN_PORT} --reload
