#!/bin/bash

ENV_FILE=/projects/goszakup/goszakup/app/core/.env

# Создание .env файла с переменными окружения
echo "HEADLESS_DRIVER=FALSE" | sudo tee $ENV_FILE > /dev/null
echo "ENVIRONMENT=LXDE" | sudo tee -a $ENV_FILE > /dev/null
