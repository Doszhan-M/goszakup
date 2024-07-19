#!/bin/bash

sudo apt install python3-tk python3-dev xvfb xclip

# Создаем переменную с путем до файла
DESKTOP_FILE=~/.config/autostart/grpc.desktop

# Проверяем существование папки autostart, если нет - создаем
if [ ! -d ~/.config/autostart ]; then
    mkdir -p ~/.config/autostart
fi

# Создаем файл .desktop с нужным содержимым
echo "[Desktop Entry]
Type=Application
Name=Goszakup
Exec=/home/asus/github/goszakup/sh/grps.sh
Terminal=false" > $DESKTOP_FILE

echo "Файл $DESKTOP_FILE успешно создан и настроен для автозагрузки."
