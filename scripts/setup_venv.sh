#!/bin/bash

# Обновление списка пакетов и установка пакета python3-venv
sudo apt update && sudo apt install python3-venv -y

# Создание виртуального окружения в текущей директории в папке venv
cd /home/asus/github/goszakup/
python3 -m venv venv

# Активация виртуального окружения
source /home/asus/github/goszakup/venv/bin/activate

# Установка зависимостей из файла requirements.txt
pip install -r requirements.txt

echo "Виртуальное окружение успешно создано и активировано. Зависимости установлены."
