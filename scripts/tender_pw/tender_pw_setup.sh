#!/bin/bash


USER="asus"
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/tender_pw/tender_pw_start.sh"
VENV_PATH="/home/$USER/github/goszakup/venv"

# Проверка на выполнение от имени пользователя (не root)
if [ "$EUID" -eq 0 ]; then
  echo "Пожалуйста, запустите скрипт от имени обычного пользователя, а не root."
  exit 1
fi

# Проверка существования виртуального окружения
if [ ! -d "$VENV_PATH" ]; then
    echo "Виртуальное окружение не найдено по пути $VENV_PATH."
fi

echo "Активиация виртуальное окружение и устанавка зависимости Playwright..."
sudo -u $USER bash <<EOF
source "$VENV_PATH/bin/activate"
playwright install --with-deps
EOF


echo "Создать пользовательский systemd сервисный файл для пользователя '$USER'"
sudo -u $USER bash <<EOF
mkdir -p /home/$USER/.config/systemd/user

SERVICE_FILE="/home/$USER/.config/systemd/user/tender_pw.service"

cat <<EOT > \$SERVICE_FILE

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

EOT

chmod 644 \$SERVICE_FILE

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable tender_pw.service

# Запуск сервиса немедленно
systemctl --user start tender_pw.service
EOF

echo "Пользовательский systemd сервис создан по пути /home/$USER/.config/systemd/user/tender_pw.service"
echo "Сервис был запущен и настроен на автозапуск при входе в систему."
echo "Вы можете управлять сервисом с помощью следующих команд (от имени пользователя '$USER'):"
echo "systemctl --user start tender_pw.service"
echo "systemctl --user stop tender_pw.service"
echo "systemctl --user restart tender_pw.service"
echo "systemctl --user status tender_pw.service"
echo "journalctl --user -u tender_pw.service -f"
