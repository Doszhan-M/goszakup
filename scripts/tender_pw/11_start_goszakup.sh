#!/bin/bash

# source ~/github/goszakup/venv/bin/activate
# cd ~/github/goszakup/goszakup
# nohup uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload &




# Загрузка переменных из файла .env
set -a
source $HOME/github/goszakup/env/tender.env
set +a

# Проверка наличия переменной WORKERS
if [ -z "$WORKERS" ]; then
  echo "Переменная WORKERS не установлена в файле .env"
  exit 1
fi

source $HOME/github/goszakup/venv/bin/activate
cd $HOME/github/goszakup/goszakup/tender_pw
uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers $WORKERS --reload
# nohup uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers $WORKERS --reload &


# kill -9 $(lsof -t -i:8000)
# uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 --reload
