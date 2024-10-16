#!/bin/bash

# Путь к кэшу NCALayer
CACHE_DIR="$HOME/.config/NCALayer/ncalayer-cache"
PLUGIN_SOURCE="$HOME/github/goszakup/scripts/files/kz.ecc.NurSignBundle_5.1.1_2e62beae-e900-4c8c-9d8e-37286ace46ec.jar"
PLUGIN_DEST="$HOME/.config/NCALayer/bundles"
NCALAYER_PATH="/home/asus/Programs/NCALayer/ncalayer.sh"
DISP=":0"

# Проверяем наличие кэша и удаляем его
if [ -d "$CACHE_DIR" ]; then
    rm -rf "$CACHE_DIR"
    echo "NCAlayer сброшен."
fi


cp "$PLUGIN_SOURCE" "$PLUGIN_DEST"
if [ $? -eq 0 ]; then
    echo "Плагин скопирован."
else
    echo "Ошибка копирования плагина." >&2
    exit 1
fi

# Настройка переменной DISPLAY
DISPLAY="$DISP"

# Запускаем NCALayer с перезапуском
env DISPLAY=$DISPLAY "$NCALAYER_PATH" --restart
if [ $? -eq 0 ]; then
    echo "NCALayer перезапущен."
else
    echo "Ошибка при перезапуске NCALayer." >&2
    exit 1
fi
