su -
usermode -aG sudo asus


sudo nano /etc/apt/sources.list
```
# Основные репозитории Debian
deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware

# Обновления безопасности
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb-src http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware

# Обновления пакетов
deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ bookworm-updates main contrib non-free non-free-firmware
```

sudo apt install vim xxd libnss3-tools -y




```
vim .zshrc
--------------------------------------------------------------
cd /home/asus/github/goszakup
source /home/asus/github/goszakup/venv/bin/activate
--------------------------------------------------------------
```

## 5. Настроить зависимости
```
pip install -r requirements.txt
```

## 6. Создать env для сервисов на основе example
```
cd $HOME/github/goszakup/scripts/
./setup_env.sh
```

## 7. Установить Docker
```
cd $HOME/github/goszakup/scripts/
./docker_debian.sh
```

## 8. Запустить сервисы из docker compose 
```
cd $HOME/github/goszakup/
docker volume create gz_redis
docker volume create gz_rabbitmq
docker compose up --build -d
```

## 9. Установить зависимости
```
cd $HOME/github/goszakup/scripts/dependencies
sudo ./dependencies.sh
```

## 10. Настроить автозапуск сервиса xvfb
```
cd $HOME/github/goszakup/scripts/display
./xvfb_config.sh
```

## 11. Настроить автозапуск сервиса VNC
```
cd $HOME/github/goszakup/scripts/display
./vnc_config.sh
```

## 12. Настроить автозапуск сервиса tender_pw
При необходимости отредактировать User и SCRIPT_PATH, потому что   
скрипт запускается от root, поэтому домашний каталог и юзер должен быть другой 
```
cd $HOME/github/goszakup/scripts/tender_pw
./tender_pw_setup.sh
```

## 13. Настроить автозапуск сервиса signer
При необходимости отредактировать User и SCRIPT_PATH, потому что   
скрипт запускается от root, поэтому домашний каталог и юзер должен быть другой 
```
cd $HOME/github/goszakup/scripts/signer
./signer_setup.sh
```