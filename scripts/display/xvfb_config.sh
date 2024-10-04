#!/bin/bash


USER="asus"
SERVICE_FILE="/home/$USER/.config/systemd/user/xvfb.service"

echo "Установка необходимых пакетов"
# sudo apt install xvfb -y


echo "Создать пользовательский systemd сервисный файл для пользователя '$USER'"
sudo -u $USER bash <<EOF
mkdir -p /home/$USER/.config/systemd/user

# Создание сервисного файла
cat <<EOT > \$SERVICE_FILE

[Unit]
Description=Virtual Framebuffer X Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always
RestartSec=5

[Install]
WantedBy=default.target


EOT

# Установка правильных прав доступа к сервисному файлу
chmod 644 \$SERVICE_FILE

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable xvfb.service

# Запуск сервиса немедленно
systemctl --user start xvfb.service
EOF

echo "DISPLAY=:99 xdpyinfo"
echo "systemctl --user start xvfb"
echo "systemctl --user stop xvfb"
echo "systemctl --user restart xvfb"
echo "systemctl --user status xvfb"
echo "journalctl --user -u xvfb -f"
