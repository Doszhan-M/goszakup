#!/bin/bash

USER="asus"
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/tender_pw/tender_pw_start.sh"
VENV_PATH="/home/$USER/github/goszakup/venv"
SERVICE_FILE="/home/$USER/.config/systemd/user/tender_pw.service"

# Проверка на выполнение от имени пользователя (не root)
if [ "$EUID" -eq 0 ]; then
  echo "Пожалуйста, запустите скрипт от имени обычного пользователя, а не root."
  exit 1
fi

# Проверка существования виртуального окружения
if [ ! -d "$VENV_PATH" ]; then
    echo "Виртуальное окружение не найдено по пути $VENV_PATH."
fi

echo "Активиация виртуального окружения и установка зависимости Playwright..."
source "$VENV_PATH/bin/activate"
playwright install --with-deps


mkdir -p "$(dirname "$SERVICE_FILE")"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=tender_pw Service
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

chmod 644 /home/$USER/.config/systemd/user/tender_pw.service

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable tender_pw.service

# Запуск сервиса немедленно
systemctl --user start tender_pw.service
EOF

echo "Пользовательский systemd сервис создан по пути $SERVICE_FILE"
echo "Сервис был запущен и настроен на автозапуск при входе в систему."
echo "systemctl --user start tender_pw"
echo "systemctl --user stop tender_pw"
echo "systemctl --user restart tender_pw"
echo "systemctl --user status tender_pw"
echo "journalctl --user -u tender_pw -f"
