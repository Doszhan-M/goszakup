#!/bin/bash

# Прерывать скрипт при ошибке
set -e

# Переменные
DISPLAY_NUMBER=99
VNC_PORT=5900
VNC_PASSWORD_FILE=/root/.vnc/passwd

# Функция для запуска Xvfb и x11vnc
start_vnc_server() {
    echo "Запуск Xvfb на DISPLAY=:$DISPLAY_NUMBER"
    Xvfb :$DISPLAY_NUMBER -screen 0 1920x1080x24 -listen tcp &
    sleep 2
    xhost +

    echo "Запуск x11vnc на DISPLAY=:$DISPLAY_NUMBER с портом $VNC_PORT"
    x11vnc -display :$DISPLAY_NUMBER -forever -shared -rfbauth $VNC_PASSWORD_FILE -noxdamage -rfbport $VNC_PORT -bg
}

# Запуск VNC-сервера
echo "Настройка и запуск VNC-сервера"
start_vnc_server

# Запуск основного приложения
echo "Запуск main.py"

export DISPLAY=:99

# exec python3 /app/main.py
exec python3 main.py
