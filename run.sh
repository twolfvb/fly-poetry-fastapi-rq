#!/bin/bash
set -e
set -x

gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000 app.main:app
