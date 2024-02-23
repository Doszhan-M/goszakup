#!/bin/bash

# Создание директории projects
sudo mkdir -p /projects

# Назначение прав доступа 777 для директории
sudo chmod -R 777 /projects

# Установка ACL прав для директории по умолчанию
sudo setfacl -m d:u::rwx /projects
sudo setfacl -m d:g::rwx /projects
sudo setfacl -m d:o::rwx /projects

# Переход в директорию projects и клонирование репозитория
cd /projects
git clone git@github.com:Doszhan-M/goszakup.git

echo "Cloning completed."

# Сделать все скрипты исполняемыми
cd /projects/goszakup/sh
find /projects/goszakup/sh -type f -name "*.sh" -exec sudo chmod +x {} \; 
