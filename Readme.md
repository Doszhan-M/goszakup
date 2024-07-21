# Install and Start  
## 1. Настроить ubuntu gnome:

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
sudo apt install xdotool  
vim ~/.config/autostart/gnome_workspace.desktop

[Desktop Entry]
Type=Application
Name=Goszakup
Exec=/home/asus/github/goszakup/scripts/gnome_workspace.sh
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

`•` Перезапустить систему


## 2. Сделать все скрипты исполняемыми
```
find /home/asus/github/goszakup/scripts/ -type f -name "*.sh" -exec sudo chmod +x {} \; 
```

## 3. Сгенерировать ssh ключи и зарегистрировать и github
```
cd /home/asus/github/goszakup/scripts/
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
cp kz.ecc.NurSignBundle_5.1.1_2e62beae-e900-4c8c-9d8e-37286ace46ec.jar /home/asus/.config/NCALayer/bundles 
``` 
После перезапуска модуль должен исчезнуть из папку bundles  

`•` Настроить автозапуск через скрипт
```
cd /home/asus/github/goszakup/scripts/
./ncalayer_config.sh
```

## 5. Установить Docker
```
cd /home/asus/github/goszakup/scripts/
./docker_install.sh
```

## 6. Запустить сервисы из docker compose 
```
cd /home/asus/github/goszakup/scripts/
docker compose up --build -d
```

## 7. Установить chromedriver если необходим 
```
cd /home/asus/github/goszakup/scripts/
./chromedriver_installer.sh
```

## 8. Настроить зависимости
```
cd /home/asus/github/goszakup/scripts/
./setup_venv.sh
```

## 9. Создать env для сервисов на основе example
```
cd /home/asus/github/goszakup/scripts/
./setup_env.sh
```

## 10. Настроить автозапуск сервиса tender_pw
```
cd /home/asus/github/goszakup/scripts/
./13_setup_goszakup.sh
```



## Порядок участия в тендере
1. Доступные действия - Создать заявку 
2. Юридический адрес -- 050061  
3. ИИК -- Банк: АО "ForteBank" ИИК: KZ5696502F0017154550 БИК: IRTYKZKA 
4. Подписать обязательные документы  
5. Сформировать документ -> Подписать через rsa ЭЦП
6. Вернуться к списку
7. Далее - Подать заявку - Да
8. Статус заявки - Подана                         

## Страницы доступа
http://127.0.0.1:8000/goszakup/docs#/  
http://127.0.0.1:8080/admin/  

http://10.192.168.10:8000/goszakup/docs#/  
http://10.192.168.10:8080/admin/
http://10.192.168.10:5554/flower_backend/tasks

http://gz.maksat.keenetic.pro/admin/
