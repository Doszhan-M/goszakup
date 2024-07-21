#!/bin/bash

source ~/github/goszakup/venv/bin/activate
cd ~/github/goszakup/goszakup
nohup uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload &

# kill -9 $(lsof -t -i:8000)
# uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload