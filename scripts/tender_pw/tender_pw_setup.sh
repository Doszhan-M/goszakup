#!/bin/bash


SCRIPT_PATH="/home/asus/github/goszakup/scripts/tender_pw/tender_pw_start.sh"
SERVICE_FILE="/etc/systemd/system/tender_pw.service"

# Проверка прав на создание файла в /etc/systemd/system
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

source /home/asus/github/goszakup/venv/bin/activate
playwright install --with-deps

# Создание файла службы
cat <<EOF > $SERVICE_FILE
[Unit]
Description=tender_pw Service
After=network.target

[Service]
Type=simple
User=asus
Environment=DISPLAY=:0
ExecStart=${SCRIPT_PATH}
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Установка прав и перезагрузка systemd
chmod 644 $SERVICE_FILE
systemctl daemon-reload
systemctl start tender_pw
systemctl enable tender_pw


echo "Systemd service file created at ${SERVICE_FILE}"
echo "You can now start and enable the service with:"
echo "sudo systemctl start tender_pw"
echo "sudo systemctl enable tender_pw"
echo "sudo systemctl disable tender_pw"
echo "sudo systemctl stop tender_pw"
echo "sudo systemctl restart tender_pw"
echo "sudo systemctl status tender_pw"
