#!/bin/bash


# Проверка прав на создание файла в /etc/systemd/system
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

SERVICE_FILE="/etc/systemd/system/ncalayer.service"


# Создаем сервисный файл с заданным содержимым
cat > "$SERVICE_FILE" <<EOF

[Unit]
Description=NCALayer Service
After=graphical.target

[Service]
Environment=DISPLAY=:0
ExecStart=$HOME/Programs/NCALayer/ncalayer.sh --restart
Restart=on-failure

[Install]
WantedBy=default.target
EOF

echo "Файл $SERVICE_FILE успешно создан."

# Перезагружаем конфигурацию systemd user
systemctl --user daemon-reload

# Включаем сервис для автозапуска при входе в систему
systemctl --user enable ncalayer.service

# Запускаем сервис немедленно
systemctl --user start ncalayer.service

echo "Сервис ncalayer запущен и настроен на автозапуск через systemd."
