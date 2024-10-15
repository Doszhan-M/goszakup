## 1. Настроить Ubuntu Gnome:

`•` Во время установки ubuntu создать пользователя с названием ```asus```
```
sudo adduser asus  
sudo usermod -aG sudo asus
Предоставить asus доступ без пароля:
sudo visudo
Добавить в конец:
asus ALL=(ALL) NOPASSWD: ALL  
```
`•` Доступ к asus через ssh  
```
ssh-copy-id asus@91.147.93.238
v6VnxyP48sveBZdXloP7iRVL0jmwJv3116Q 
```
`•` Установить Gnome:
```
sudo apt update
sudo apt install tmux htop vim curl wget libnss3-tools unzip git gnome-screenshot -y
sudo apt upgrade -y  
sudo reboot
tmux new -t gz
sudo apt update  
sudo apt install ubuntu-gnome-desktop -y && sudo reboot
tmux attach -t gz
```
`•` Установить noMachine:
```
wget https://download.nomachine.com/download/8.13/Linux/nomachine_8.13.1_1_amd64.deb
sudo dpkg -i no
```
`•` Установить chrome:
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i go
```
`•` Установить gnome-software:
```
sudo apt install gnome-software
```
`•` Отключить системные звуки:
```
gsettings set org.gnome.desktop.sound event-sounds false
```
`•` Переключиться на Xorg сервер на окне входа!

`•` Чтобы рабочии стол стал активным после перезапуска:
Multitasking -> Workspaces установить фиксированное количество раб столов на 1.  

`•` Необходимо настроить автологин в настройках и отключить блокировку когда гаснет экран:  
Privacy and Security -> Screen Lock. 

`•` Надо включить автологин:
System -> User ->  Automatic login

`•` Чтобы chrome не запрашивал keyring после перезагрузки, можно удалить:
```
sudo apt remove gnome-keyring 
```

`•` Если это ноутбук:  
Установка таймаута для выключения экрана на 5 часов  
```
gsettings set org.gnome.desktop.session idle-delay 18000
gsettings get org.gnome.desktop.session idle-delay
```
Чтобы при закрытии крышки, ноут не уходил в сон, отредактировать:
```
sudo vim /etc/systemd/logind.conf
```  
Если HandleLidSwitch не установлен на ignore затем изменить его:
HandleLidSwitch=ignore

`•` Перезапустить систему


## 2. Сделать все скрипты исполняемыми
```
find $HOME/github/goszakup/scripts/ -type f -name "*.sh" -exec sudo chmod +x {} \; 
```

## 3. Настроить автозапуск gnome_workspace.sh:
```
cd $HOME/github/goszakup/scripts/
sudo ./gnome_workspace_setup.sh
После перезапуска можно проверить логи:
cat /tmp/workspace_selection.log 
```

## 4. Установить NCALayer
`•` Скачать NCALayer из офф сайта и установить п папку Programs.  
Если есть ошибка на xdd, то установить xdd:
```
sudo apt install xxd -y
```
`•` Проверить модуль гос закупок на этих сайтах:  
https://mhelp.kz/ncalayer-skachat/#google_vignette  
https://pki.gov.kz/docs/nl_ru/bundles/#_2  
Всегда надо использовать последнюю версию.  
Скопировать разархивированный jar файл в папку bundles:  
```
cd $HOME/github/goszakup/scripts/files/
cp kz.ecc.NurSignBundle_5.1.1_2e62beae-e900-4c8c-9d8e-37286ace46ec.jar $HOME/.config/NCALayer/bundles 
``` 
После перезапуска модуль должен исчезнуть из папку bundles  

`•` Служба signer сам выполняет автозапуск NCALayer, при необходимости можно настроить автозапуск через скрипт
```
cd $HOME/github/goszakup/scripts/
./ncalayer_config.sh
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
./docker_install.sh
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
