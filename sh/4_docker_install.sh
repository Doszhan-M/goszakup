#!/bin/bash

# Обновление списка пакетов и их версий
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg -y

# Добавление GPG ключа репозитория Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавление репозитория Docker в список источников пакетов
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Обновление списка пакетов после добавления нового репозитория
sudo apt update

# Установка Docker CE
sudo apt install docker-ce -y

# Запуск и добавление Docker в автозагрузку
sudo systemctl start docker
sudo systemctl enable docker

# Добавление текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Вывод версии Docker для проверки успешной установки
docker --version

# Инструкция по перезагрузке
echo "Docker установлен. Перезайдите в систему (или перезапустите терминал), чтобы завершить установку и применить изменения группы."

sudo reboot
