#!/bin/bash

# Имя пользователя
USER="asus"

# Путь к скрипту, который будет запускаться сервисом
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/signer/signer_start.sh"

# Проверка прав на выполнение скрипта (должен быть запущен как root)
if [ "$(id -u)" -ne 0 ]; then
    echo "Этот скрипт должен быть запущен с правами root."
    exit 1
fi

# Установка необходимых пакетов
apt-get update
apt-get install -y python3-tk python3-dev xclip dbus-x11

# Создание директории для пользовательских сервисов, если она не существует
mkdir -p /home/$USER/.config/systemd/user

# Определение пути к сервисному файлу
SERVICE_FILE="/home/$USER/.config/systemd/user/signer.service"

# Создание сервисного файла
cat <<EOT > \$SERVICE_FILE
[Unit]
Description=Signer Service
After=graphical.target

[Service]
Type=simple
ExecStart=$SCRIPT_PATH
Restart=on-failure
RestartSec=5
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
Environment=HOME=/home/$USER
Environment=PATH=/usr/bin:/usr/local/bin

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
echo "  systemctl --user start signer.service"
echo "  systemctl --user stop signer.service"
echo "  systemctl --user restart signer.service"
echo "  systemctl --user status signer.service"
echo "  journalctl --user -u signer.service -f"
