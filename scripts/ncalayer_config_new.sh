#!/bin/bash

# Проверка прав на создание файла в /etc/systemd/system
if [ "$(id -u)" -ne 0 ]; then
    echo "Этот скрипт должен быть запущен с правами root."
    exit 1
fi

apt update && apt install dbus-x11

# Укажите пользователя, от имени которого будет запускаться сервис
SERVICE_USER="asus"

# Получаем домашнюю директорию пользователя
USER_HOME=$(eval echo "~$SERVICE_USER")

SERVICE_FILE="/etc/systemd/system/ncalayer.service"

# Создаем сервисный файл с заданным содержимым
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=NCALayer Service
After=graphical.target
Requires=graphical.target

[Service]
Type=simple
User=asus
Group=asus
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/asus/.Xauthority
Environment=HOME=/home/asus
ExecStart=/home/asus/Programs/NCALayer/ncalayer.sh --run
ExecStop=/home/asus/Programs/NCALayer/ncalayer.sh --stop
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
EOF

echo "Файл $SERVICE_FILE успешно создан."

# Перезагружаем конфигурацию systemd
systemctl daemon-reload

# Включаем сервис для автозапуска при загрузке системы
systemctl enable ncalayer.service

# Запускаем сервис немедленно
systemctl start ncalayer.service

echo "Сервис ncalayer запущен и настроен на автозапуск через systemd."
