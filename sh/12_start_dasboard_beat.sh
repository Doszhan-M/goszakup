#!/bin/bash

source /projects/goszakup/venv/bin/activate
cd /projects/goszakup/dashboard
watchfiles --filter python 'celery -A core worker -Q beat_tasks -B --pool=prefork --concurrency=4 --max-tasks-per-child=1'