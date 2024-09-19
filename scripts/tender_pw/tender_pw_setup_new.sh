#!/bin/bash

# Имя пользователя
USER="asus"
SCRIPT_PATH="/home/$USER/github/goszakup/scripts/tender_pw/tender_pw_start.sh"
VENV_PATH="/home/$USER/github/goszakup/venv"
SERVICE_NAME="tender_pw.service"

# Проверка прав на выполнение скрипта (должен быть запущен как root)
if [ "$(id -u)" -ne 0 ]; then
    echo "Этот скрипт должен быть запущен с правами root."
    exit 1
fi

# echo "Устанавливаем необходимые пакеты..."
# apt-get update
# apt-get install -y python3-tk python3-dev xclip dbus-x11

# # Проверка существования виртуального окружения
# if [ ! -d "$VENV_PATH" ]; then
#     echo "Виртуальное окружение не найдено по пути $VENV_PATH."
# fi

# echo "Активируем виртуальное окружение и устанавливаем зависимости Playwright..."
# sudo -u $USER bash <<EOF
# source "$VENV_PATH/bin/activate"
# playwright install --with-deps
# EOF

echo "Создаём пользовательский systemd сервисный файл для пользователя '$USER'..."

# Создание пользовательского systemd сервисного файла
sudo -u $USER bash <<EOF
mkdir -p /home/$USER/.config/systemd/user

SERVICE_FILE="/home/$USER/.config/systemd/user/$SERVICE_NAME"

cat <<EOT > \$SERVICE_FILE
[Unit]
Description=tender_pw Service
After=graphical.target

[Service]
Type=simple
ExecStart=$SCRIPT_PATH
Restart=on-failure
RestartSec=5
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
Environment=HOME=/home/$USER
Environment=PATH=/usr/bin:/usr/local/bin:$VENV_PATH/bin

[Install]
WantedBy=default.target
EOT

chmod 644 \$SERVICE_FILE

# Перезагрузка конфигурации systemd для пользователя
systemctl --user daemon-reload

# Включение сервиса для автозапуска при входе в систему
systemctl --user enable "$SERVICE_NAME"

# Запуск сервиса немедленно
systemctl --user start "$SERVICE_NAME"
EOF

echo "Пользовательский systemd сервис создан по пути /home/$USER/.config/systemd/user/$SERVICE_NAME"
echo "Сервис был запущен и настроен на автозапуск при входе в систему."
echo "Вы можете управлять сервисом с помощью следующих команд (от имени пользователя '$USER'):"
echo "  systemctl --user start $SERVICE_NAME"
echo "  systemctl --user stop $SERVICE_NAME"
echo "  systemctl --user restart $SERVICE_NAME"
echo "  systemctl --user status $SERVICE_NAME"
echo "  journalctl --user -u $SERVICE_NAME -f"
