#!/bin/bash

sudo apt update && sudo apt upgrade -y && sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg -y && curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list  /dev/null && apt-cache policy docker-ce && sudo apt update && sudo apt install docker-ce -y && sudo systemctl start docker && sudo systemctl enable docker && sudo usermod -aG docker ${USER} && sudo su - ${USER} && id -nG

docker --version

echo "Docker установлен. Перезайдите в систему (или перезапустите терминал), чтобы завершить установку и применить изменения группы."

sudo reboot
