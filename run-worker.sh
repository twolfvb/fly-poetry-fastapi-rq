#!/bin/bash
set -e
set -x

#poetry run rq worker
poetry run celery -A app.celery.celery worker -l info
