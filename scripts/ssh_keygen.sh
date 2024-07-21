#!/bin/bash

# Генерация нового SSH ключа с использованием значений по умолчанию
ssh-keygen -q -t rsa -b 2048 -N "" -f ~/.ssh/id_rsa <<< ""

# Вывод публичного ключа
echo "Ваш публичный ключ SSH:"
cat ~/.ssh/id_rsa.pub
