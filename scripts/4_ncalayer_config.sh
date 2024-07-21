#!/bin/bash

# Определяем путь к директории автозапуска
AUTOSTART_DIR="$HOME/.config/autostart"

# Создаем директорию, если она не существует
mkdir -p "$AUTOSTART_DIR"

# Определяем путь к файлу .desktop
DESKTOP_FILE="$AUTOSTART_DIR/ncalayer.desktop"

# Создаем .desktop файл с заданным содержимым
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.3
Name=NCALayer
Name[ru]=NCALayer
GenericName=NCALayer
GenericName[ru]=NCALayer
Comment=NCALayer application
Comment[ru]=Приложение для работы с ЭЦП
Icon=ncalayer
Type=Application
Terminal=false
Categories=Network;RemoteAccess
Exec="/home/asus/Programs/NCALayer/ncalayer.sh" --run
EOF

echo "Файл $DESKTOP_FILE успешно создан."
