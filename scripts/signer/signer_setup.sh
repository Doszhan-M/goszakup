#!/bin/bash

SCRIPT_PATH="/home/debian/github/goszakup/scripts/signer/signer_start.sh"
SERVICE_FILE="/etc/systemd/system/signer.service"

# Проверка прав на создание файла в /etc/systemd/system
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

# Создание файла службы
cat <<EOF > $SERVICE_FILE
[Unit]
Description=signer Service
After=network.target

[Service]
Type=simple
User=debian
Environment=DISPLAY=:0
ExecStart=${SCRIPT_PATH}
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Установка прав и перезагрузка systemd
chmod 644 $SERVICE_FILE
systemctl daemon-reload
systemctl start signer
systemctl enable signer


echo "Systemd service file created at ${SERVICE_FILE}"
echo "You can now start and enable the service with:"
echo "sudo systemctl start signer"
echo "sudo systemctl enable signer"
echo "sudo systemctl disable signer"
echo "sudo systemctl stop signer"
echo "sudo systemctl restart signer"
echo "sudo systemctl status signer"
