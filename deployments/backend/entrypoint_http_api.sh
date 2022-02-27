#!/usr/bin/env bash

set -e
if [ -z "$API_PORT" ]; then
  API_PORT=8082
fi
if [ -z "$ADDITIONAL_API_ARGS" ]; then
  ADDITIONAL_API_ARGS=""
fi
if [ -z "$API_LOG_LEVEL" ]; then
  API_LOG_LEVEL=info
fi

GUNICORN_CMD_ARGS="--bind=0.0.0.0:${API_PORT} --log-level=${API_LOG_LEVEL} --workers=1 --error-logfile=- --access-logfile=- --forwarded-allow-ip='*' --proxy-allow-from='*' ${ADDITIONAL_API_ARGS} -t 1200"
export GUNICORN_CMD_ARGS

gunicorn questionnaire.composites.http_api:app