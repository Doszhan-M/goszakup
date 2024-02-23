#!/bin/bash

# Останавить работающие сервисы
kill -9 $(lsof -t -i:8000)
kill -9 $(lsof -t -i:8080)
pkill -f "celery -A core worker -Q beat_tasks -B"

# Запустить сервисы
nohup ./10_start_goszakup.sh > /dev/null 2>&1 &
nohup ./11_start_dashboard.sh > /dev/null 2>&1 &
nohup ./12_start_dasboard_beat.sh > /dev/null 2>&1 &
nohup ./13_start_ncalayer.sh > /dev/null 2>&1 &
wait
