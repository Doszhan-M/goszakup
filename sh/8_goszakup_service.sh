#!/bin/bash

# Создание systemd сервиса для FastAPI приложения с использованием venv

SERVICE_FILE=/etc/systemd/system/goszakup.service
ENV_FILE=/projects/goszakup/goszakup/app/core/.env

# Создание .env файла с переменными окружения
echo "HEADLESS_DRIVER=TRUE" | sudo tee $ENV_FILE > /dev/null
echo "ENVIRONMENT=LXDE" | sudo tee -a $ENV_FILE > /dev/null
echo "DISPLAY=:0" | sudo tee -a $ENV_FILE > /dev/null

# Определение пути к виртуальному окружению и Gunicorn
VENV_PATH=/projects/goszakup/venv
GUNICORN_PATH=$VENV_PATH/bin/gunicorn

# Создание файла сервиса
cat <<EOF | sudo tee $SERVICE_FILE > /dev/null
[Unit]
Description=FastAPI App - Goszakup
After=network.target

[Service]
User=$(whoami)
Group=$(whoami)
WorkingDirectory=/projects/goszakup/goszakup
ExecStart=$GUNICORN_PATH -w 2 -k uvicorn.workers.UvicornWorker --reload app.core.main:app --bind 0.0.0.0:8000
Environment="PATH=$VENV_PATH/bin"
EnvironmentFile=$ENV_FILE
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd для применения нового конфига
sudo systemctl daemon-reload

# Включение автозагрузки сервиса
sudo systemctl enable goszakup

# Запуск сервиса
sudo systemctl start goszakup

echo "Сервис goszakup создан и запущен"
