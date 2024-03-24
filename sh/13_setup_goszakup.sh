#!/bin/bash

sudo apt install python3-tk python3-dev xvfb

# Создаем переменную с путем до файла
DESKTOP_FILE=~/.config/autostart/goszakup.desktop

# Проверяем существование папки autostart, если нет - создаем
if [ ! -d ~/.config/autostart ]; then
    mkdir -p ~/.config/autostart
fi

# Создаем файл .desktop с нужным содержимым
echo "[Desktop Entry]
Type=Application
Name=Goszakup
Exec=/projects/goszakup/sh/12_launch_goszakup.sh
Terminal=false" > $DESKTOP_FILE

echo "Файл $DESKTOP_FILE успешно создан и настроен для автозагрузки."
