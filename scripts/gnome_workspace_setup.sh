#!/bin/bash

USER="asus"
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/gnome_workspace.sh"
SERVICE_FILE="/etc/systemd/system/gnome_workspace.service"

# Проверка прав на создание файла в /etc/systemd/system
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

# Убедитесь, что xdotool установлен
sudo apt-get install xdotool -y

# Создание файла службы
cat <<EOF > $SERVICE_FILE
[Unit]
Description=Gnome Workspace Selection Service
After=graphical.target

[Service]
Type=simple
User=$USER
Environment=DISPLAY=:0
ExecStart=${SCRIPT_PATH}
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Установка прав и перезагрузка systemd
chmod 644 $SERVICE_FILE
systemctl daemon-reload
systemctl start gnome_workspace
systemctl enable gnome_workspace

echo "Systemd service file created at ${SERVICE_FILE}"
echo "You can now start and enable the service with:"
echo "sudo systemctl start gnome_workspace"
echo "sudo systemctl enable gnome_workspace"
echo "sudo systemctl disable gnome_workspace"
echo "sudo systemctl stop gnome_workspace"
echo "sudo systemctl restart gnome_workspace"
echo "sudo systemctl status gnome_workspace"
echo "journalctl -u gnome_workspace -f"
