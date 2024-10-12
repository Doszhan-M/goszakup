#!/bin/bash

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg -y

# Добавление ключа для Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавление репозитория Docker для Debian
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Обновление списка пакетов с новыми репозиториями
sudo apt update

# Проверка доступности пакета docker-ce
apt-cache policy docker-ce

# Установка Docker
sudo apt install docker-ce -y

# Запуск и включение Docker в автозапуск
sudo systemctl start docker
sudo systemctl enable docker

# Добавление текущего пользователя в группу docker
sudo usermod -aG docker ${USER}

# Перезапуск пользователя для применения изменений группы
sudo su - ${USER}
id -nG

# Проверка версии Docker
docker --version

# Сообщение об установке
echo "Docker установлен. Перезайдите в систему (или перезапустите терминал), чтобы завершить установку и применить изменения группы."

# Перезагрузка системы
sudo reboot
