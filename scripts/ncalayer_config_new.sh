#!/bin/bash



# Определяем путь к директории systemd user services
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# Создаем директорию, если она не существует
mkdir -p "$SYSTEMD_USER_DIR"

# Определяем путь к файлу сервиса
SERVICE_FILE="$SYSTEMD_USER_DIR/ncalayer.service"

# Создаем сервисный файл с заданным содержимым
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=NCALayer Service
After=graphical.target

[Service]
Type=simple
ExecStart=/home/asus/Programs/NCALayer/ncalayer.sh --run
Restart=on-failure
Environment=DISPLAY=:0
Environment=HOME=/home/asus

[Install]
WantedBy=default.target
EOF

echo "Файл $SERVICE_FILE успешно создан."

# Перезагружаем конфигурацию systemd user
systemctl --user daemon-reload

# Включаем сервис для автозапуска при входе в систему
systemctl --user enable ncalayer.service

# Запускаем сервис немедленно
systemctl --user start ncalayer.service

echo "Сервис ncalayer запущен и настроен на автозапуск через systemd."
