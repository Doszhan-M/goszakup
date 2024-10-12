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



## 7. Установить Docker
```
cd $HOME/github/goszakup/scripts/
./docker_debian.sh
```