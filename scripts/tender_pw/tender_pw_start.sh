#!/bin/bash

# Загрузка переменных из файла .env
set -a
source $HOME/github/goszakup/env/tender.env
set +a

# Проверка наличия переменной WORKERS
if [ -z "$WORKERS" ]; then
    echo "Переменная WORKERS не установлена в файле .env"
    exit 1
fi

# Установка DISPLAY для доступа к X серверу
export DISPLAY=:99

source $HOME/github/goszakup/venv/bin/activate
cd $HOME/github/goszakup/tender_pw
eval "watchfiles --filter python 'uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers $WORKERS'"
