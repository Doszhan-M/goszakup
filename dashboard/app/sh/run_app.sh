#!/bin/bash

python3 manage.py migrate

echo "------------------------------------------------------------------------------------"
echo "START DASHBOARD"
echo "------------------------------------------------------------------------------------"

gunicorn --workers=1 core.wsgi --bind 0.0.0.0:8080 --log-level=info --access-logfile '-' --error-logfile '-' --access-logformat "%(m)s: %(U)s - %(s)s" --reload
