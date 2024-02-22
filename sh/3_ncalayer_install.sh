#!/bin/bash

cd /projects/goszakup/sh/ncalayer
unzip ncalayer.zip -d installer
cd installer
# Запуск скрипта установки с автоматическим ответом "Yes" на вопросы
yes Yes | ./ncalayer.sh --nogui

# chmod +x 3.ncalayer.sh
# ./3.ncalayer.sh.sh
