#!/bin/bash

# Обновление списка пакетов
sudo apt update && sudo apt install wget curl jq unzip gnome-screenshot -y

# Скачивание и установка Google Chrome
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt install ./google-chrome-stable_current_amd64.deb -y

# Получение URL последней версии Chromedriver
wget https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json -O json_data.json
CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform == "linux64") | .url' json_data.json)

# Скачивание и распаковка Chromedriver
wget "$CHROMEDRIVER_URL" -O chromedriver.zip
sudo unzip -j ./chromedriver.zip 'chromedriver-linux64/chromedriver' -d /usr/local/bin/

# Очистка
# rm ./google-chrome-stable_current_amd64.deb
rm ./chromedriver.zip
rm ./json_data.json

echo "Google Chrome и Chromedriver успешно установлены."
