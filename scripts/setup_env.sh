#!/bin/bash

# Папка, в которой находятся файлы .example
DIRECTORY="~/github/goszakup/env"

# Перебираем все файлы с расширением .example в указанной папке
for file in "$DIRECTORY"/*.example; do
  # Проверяем, что файл существует и имеет расширение .example
  if [[ -f "$file" ]]; then
    # Создаем новый файл с расширением .env
    new_file="${file%.example}.env"
    cp "$file" "$new_file"
    echo "Создан файл: $new_file"
  fi
done
