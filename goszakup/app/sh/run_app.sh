#!/bin/bash


if [[ "$DEPLOY" = "TRUE" ]]; then
    echo "RUNNING DEPLOY"
    uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 4
else
    echo "RUNNING DEVELOPMENT"
    uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload
fi
