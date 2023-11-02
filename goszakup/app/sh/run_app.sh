#!/bin/bash


if [[ "$DEPLOY" = "TRUE" ]]; then
    echo "RUNNING DEPLOY"
    # gunicorn app.core.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1
else
    echo "RUNNING TEST"
    uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload
fi
