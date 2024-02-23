#!/bin/bash

source /projects/goszakup/venv/bin/activate
cd /projects/goszakup/goszakup
nohup uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 &

# kill -9 $(lsof -t -i:8000)
# uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload