#!/bin/bash

# Обновление списка пакетов и установка пакета python3-venv
sudo apt update && sudo apt install python3-venv python3-pip python3-xyz -y

# Создание виртуального окружения в текущей директории в папке venv
cd $HOME/github/goszakup/
# python3 -m venv venv

# Активация виртуального окружения
# source $HOME/github/goszakup/venv/bin/activate

# Установка зависимостей из файла requirements.txt
pip install -r requirements.txt

echo "Зависимости установлены."
