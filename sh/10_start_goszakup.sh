#!/bin/bash
source /projects/goszakup/venv/bin/activate
cd /projects/goszakup/goszakup
uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload
