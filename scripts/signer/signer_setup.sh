#!/bin/bash


USER="asus"
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/signer/signer_start.sh"
SERVICE_FILE="/home/$USER/.config/systemd/user/signer.service"

# Проверка на выполнение от имени пользователя (не root)
if [ "$EUID" -eq 0 ]; then
  echo "Пожалуйста, запустите скрипт от имени обычного пользователя, а не root."
  exit 1
fi

echo "Создать пользовательский systemd сервисный файл для пользователя '$USER'"

mkdir -p "$(dirname "$SERVICE_FILE")"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Signer Service
After=graphical.target xvfb.service
Requires=xvfb.service

[Service]
Type=simple
ExecStart=$SCRIPT_PATH
Environment=DISPLAY=:99
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Установка правильных прав доступа к сервисному файлу
chmod 644 /home/$USER/.config/systemd/user/signer.service

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable signer.service

# Запуск сервиса немедленно
systemctl --user start signer.service

echo "Пользовательский systemd сервис создан по пути $SERVICE_FILE"
echo "Сервис был запущен и настроен на автозапуск при входе в систему."
echo "systemctl --user start signer"
echo "systemctl --user stop signer"
echo "systemctl --user restart signer"
echo "systemctl --user status signer"
echo "journalctl --user -u signer -f"
