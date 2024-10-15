#!/bin/bash


USER="asus"
SERVICE_FILE="/home/$USER/.config/systemd/user/xvfb.service"

# Проверка на выполнение от имени пользователя (не root)
if [ "$EUID" -eq 0 ]; then
  echo "Пожалуйста, запустите скрипт от имени обычного пользователя, а не root."
  exit 1
fi

mkdir -p "$(dirname "$SERVICE_FILE")"

cat <<EOF > "$SERVICE_FILE"
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
EOF

# Установка правильных прав доступа к сервисному файлу
chmod 644 /home/$USER/.config/systemd/user/xvfb.service

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable xvfb.service

# Запуск сервиса немедленно
systemctl --user start xvfb.service

echo "DISPLAY=:99 xdpyinfo"
echo "systemctl --user start xvfb"
echo "systemctl --user stop xvfb"
echo "systemctl --user restart xvfb"
echo "systemctl --user status xvfb"
echo "journalctl --user -u xvfb -f"
