#!/bin/bash


USER="asus"
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/signer/signer_start.sh"
SERVICE_FILE="/home/$USER/.config/systemd/user/signer.service"

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

echo "Установка необходимых пакетов"
apt-get update && apt-get install -y python3-tk python3-dev xclip dbus-x11

echo "Создать пользовательский systemd сервисный файл для пользователя '$USER'"
sudo -u $USER bash <<EOF
mkdir -p /home/$USER/.config/systemd/user

# Создание сервисного файла
cat <<EOT > \$SERVICE_FILE
[Unit]
Description=Signer Service
After=graphical.target

[Service]
Type=simple
ExecStart=$SCRIPT_PATH
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
Environment=HOME=/home/$USER
Environment=PATH=/usr/bin:/usr/local/bin
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOT

# Установка правильных прав доступа к сервисному файлу
chmod 644 \$SERVICE_FILE

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable signer.service

# Запуск сервиса немедленно
systemctl --user start signer.service
EOF

echo "Пользовательский systemd сервис создан по пути /home/$USER/.config/systemd/user/signer.service"
echo "Сервис был запущен и настроен на автозапуск при входе в систему."
echo "Вы можете управлять сервисом с помощью следующих команд (от имени пользователя 'asus'):"
echo "systemctl --user start signer.service"
echo "systemctl --user stop signer.service"
echo "systemctl --user restart signer.service"
echo "systemctl --user status signer.service"
echo "journalctl --user -u signer.service -f"
