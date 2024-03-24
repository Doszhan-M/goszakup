#!/bin/bash

ENV_FILE=/projects/goszakup/goszakup/app/core/.env

# Создание .env файла с переменными окружения
echo "DISPLAY=:99" | sudo tee -a $ENV_FILE > /dev/null
