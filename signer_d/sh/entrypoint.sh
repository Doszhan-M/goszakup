#!/bin/bash

# Прерывать скрипт при ошибке
set -e


# Запуск supervisord в фоне
echo "Запуск supervisord"
supervisord -c /etc/supervisor/conf.d/supervisord.conf &

nginx -g 'daemon off;' &

# Установка переменной DISPLAY
export DISPLAY=:99

# Запуск основного приложения
echo "Запуск main.py"
sleep 3
exec python3 /app/main.py

# Переменные
# DISPLAY_NUMBER=99
# VNC_PORT=5900
# VNC_PASSWORD_FILE=/root/.vnc/passwd

# # Функция для остановки существующих процессов Xvfb и x11vnc
# cleanup_existing_services() {
#     echo "Остановка существующих процессов Xvfb и x11vnc, если они есть."

#     # Остановка Xvfb, если он запущен
#     if pgrep Xvfb > /dev/null; then
#         echo "Найден существующий процесс Xvfb. Завершение..."
#         pkill Xvfb
#         sleep 1
#     fi

#     # Остановка x11vnc, если он запущен
#     if pgrep x11vnc > /dev/null; then
#         echo "Найден существующий процесс x11vnc. Завершение..."
#         pkill x11vnc
#         sleep 1
#     fi

#     # Удаление блокировочного файла Xvfb, если он существует
#     if [ -e "$XVFB_LOCK_FILE" ]; then
#         echo "Удаление блокировочного файла: $XVFB_LOCK_FILE"
#         rm -f "$XVFB_LOCK_FILE"
#     fi
# }

# # Функция для запуска Xvfb и x11vnc
# start_vnc_server() {
#     echo "Запуск Xvfb на DISPLAY=:$DISPLAY_NUMBER"
#     rm -r /tmp/.X99-lock
#     Xvfb :$DISPLAY_NUMBER -screen 0 1920x1080x24 &

#     echo "Запуск x11vnc на DISPLAY=:$DISPLAY_NUMBER с портом $VNC_PORT"
#     x11vnc -display :$DISPLAY_NUMBER -forever -shared -rfbauth $VNC_PASSWORD_FILE -noxdamage -rfbport $VNC_PORT -bg
# }

# # Очистка перед запуском
# cleanup_existing_services

# # Запуск VNC-сервера
# echo "Настройка и запуск VNC-сервера"
# start_vnc_server

# /usr/bin/supervisord

# # Запуск основного приложения
# echo "Запуск main.py"
# export DISPLAY=:99
# exec python3 /app/main.py
# exec python3 main.py
