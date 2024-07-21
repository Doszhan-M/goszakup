#!/bin/bash

# Обновление списка пакетов и установка пакета python3-venv, если он еще не установлен
sudo apt update
sudo apt install python3-venv -y

# Создание виртуального окружения в текущей директории в папке venv
cd /projects/goszakup/
python3 -m venv venv

# Активация виртуального окружения
source /projects/goszakup/venv/bin/activate

# Установка зависимостей из файла requirements.txt
pip install -r requirements.txt

echo "Виртуальное окружение успешно создано и активировано. Зависимости установлены."
