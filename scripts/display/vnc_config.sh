#!/bin/bash


set -e  # Прерывать скрипт при ошибке

# Переменные
VNC_PASSWORD="Doszhan89!"  # Пароль для VNC-доступа
VNC_PASSWORD_FILE="$HOME/.vnc/passwd"
SERVICE_FILE="$HOME/.config/systemd/user/x11vnc.service"

# Проверка на выполнение от имени пользователя (не root)
if [ "$EUID" -eq 0 ]; then
  echo "Пожалуйста, запустите скрипт от имени обычного пользователя, а не root."
  exit 1
fi

# # Обновление списка пакетов и установка x11vnc
# echo "Обновление списка пакетов..."
# sudo apt-get update

# echo "Установка x11vnc..."
# sudo apt-get install -y x11vnc

# Настройка пароля VNC
if [ ! -f "$VNC_PASSWORD_FILE" ]; then
  echo "Создание файла пароля VNC..."
  mkdir -p "$(dirname "$VNC_PASSWORD_FILE")"
  echo "$VNC_PASSWORD" | x11vnc -storepasswd /dev/stdin "$VNC_PASSWORD_FILE"
  chmod 600 "$VNC_PASSWORD_FILE"
  echo "Файл пароля VNC создан по пути $VNC_PASSWORD_FILE."
else
  echo "Файл пароля VNC уже существует: $VNC_PASSWORD_FILE."
fi

# # Создание systemd-сервиса для x11vnc
# echo "Создание systemd-сервиса для x11vnc..."

# mkdir -p "$(dirname "$SERVICE_FILE")"

# cat <<EOF > "$SERVICE_FILE"
# [Unit]
# Description=Start x11vnc at startup
# After=graphical.target xvfb.service
# Requires=xvfb.service

# [Service]
# Type=simple
# ExecStart=/usr/bin/x11vnc -display :99 -forever -shared -rfbauth /home/asus/.vnc/passwd -noxdamage
# Environment=DISPLAY=:99
# Restart=on-failure
# RestartSec=5

# [Install]
# WantedBy=default.target
# EOF

# echo "Systemd-сервис для x11vnc создан по пути $SERVICE_FILE."

# # Перезагрузка systemd конфигурации пользователя
# echo "Перезагрузка systemd конфигурации пользователя..."
# systemctl --user daemon-reload

# # Включение и запуск сервиса x11vnc
# echo "Включение и запуск сервиса x11vnc..."
# systemctl --user enable x11vnc.service
# systemctl --user start x11vnc.service

# echo "x11vnc настроен и запущен."

# # Инструкции для пользователя
# echo "Проверьте статус сервиса x11vnc с помощью команды:"
# echo "  systemctl --user status x11vnc.service"
# echo "  systemctl --user restart x11vnc.service"

# echo "Если требуется, разрешите доступ через брандмауэр для порта 5900:"
# echo "  sudo ufw allow 5900/tcp"
