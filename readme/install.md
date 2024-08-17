## 1. Настроить Ubuntu Gnome:

`•` Во время установки ubuntu создать пользователя с названием ```asus```

```
sudo apt update && sudo apt upgrade -y  
sudo apt -y install htop vim curl wget libnss3-tools unzip git gnome-screenshot
```
`•` Переключиться на Xorg сервер на окне входа!

`•` Чтобы рабочии стол стал активным после перезапуска, необходимо в настройках
Multitasking -> Workspaces установить фиксированное количество раб столов на 1,
необходимо настроить автологин в настройках и отключить блокировку когда гаснет экран:
Privacy and Security -> Screen Lock.
Настроить автозапуск gnome_workspace.sh:
```
sudo apt install xdotool -y  
vim ~/.config/autostart/gnome_workspace.desktop

[Desktop Entry]
Type=Application
Name=Goszakup
Exec=$HOME/github/goszakup/scripts/gnome_workspace.sh
Terminal=false
```  

`•` Чтобы при закрытии крышки, ноут не уходил в сон, отредактировать:
```
sudo vim /etc/systemd/logind.conf
```  
Если HandleLidSwitch не установлен на ignore затем изменить его:
HandleLidSwitch=ignore

`•` Чтобы chrome не запрашивал keyring после перезагрузки, можно удалить:
```
sudo apt remove gnome-keyring 
```

`•` Установка таймаута для выключения экрана на 5 часов
```
gsettings set org.gnome.desktop.session idle-delay 18000
gsettings get org.gnome.desktop.session idle-delay
```

`•` Перезапустить систему


## 2. Сделать все скрипты исполняемыми
```
find $HOME/github/goszakup/scripts/ -type f -name "*.sh" -exec sudo chmod +x {} \; 
```

## 3. Сгенерировать ssh ключи и зарегистрировать и github
```
cd $HOME/github/goszakup/scripts/
sudo ./ssh_keygen.sh
```

## 4. Установить NCALayer


`•` Скачать NCALayer из офф сайта и установить п папку Programs.  
Если есть ошибка на xdd, то установить xdd:
```
sudo apt install xdd -y
```
`•` Проверить модуль гос закупок на этих сайтах:  
https://mhelp.kz/ncalayer-skachat/#google_vignette  
https://pki.gov.kz/docs/nl_ru/bundles/#_2  
Всегда надо использовать последнюю версию.  
Скопировать разархивированный jar файл в папку bundles:  
```
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
cd $HOME/github/goszakup/scripts/
./setup_req.sh
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

## 9. Настроить автозапуск сервиса tender_pw
При необходимости отредактировать User и SCRIPT_PATH, потому что   
скрипт запускается от root, поэтому домашний каталог и юзер должен быть другой 
```
cd $HOME/github/goszakup/scripts/tender_pw
./tender_pw_setup.sh
```

## 9. Настроить автозапуск сервиса signer
При необходимости отредактировать User и SCRIPT_PATH, потому что   
скрипт запускается от root, поэтому домашний каталог и юзер должен быть другой 
```
cd $HOME/github/goszakup/scripts/signer
./signer_setup.sh
```


