#!/bin/bash
source /projects/goszakup/venv/bin/activate
cd /projects/goszakup/dashboard
kill -9 $(lsof -t -i:8080)
gunicorn --workers=1 core.wsgi --bind 0.0.0.0:8080 --log-level=info --access-logfile '-' --error-logfile '-' --access-logformat "%(m)s: %(U)s - %(s)s" --reload