# Install and Start
1. Настроить gnome:
```
su -  
apt update && apt upgrade -y  
apt install sudo  
usermod -aG sudo linux  
reboot  

sudo apt update && sudo apt upgrade -y  
sudo apt -y install htop vim curl wget libnss3-tools unzip

Чтобы рабочии стол стал активным после перезапуска, необходимо в настройках
Multitasking-Workspaces установить фиксированное количество раб столов на 1,
также необходимо настроить автологин в настройках

Чтобы при закрытии крышки, ноут не уходил в сон, отредактировать:
sudo vim /etc/systemd/logind.conf  
Если HandleLidSwitch не установлен на ignore затем измените его:
HandleLidSwitch=ignore

Чтобы chrome не запрашивал keyring после перезагрузки, можно удалить:
sudo apt remove gnome-keyring 

Перезапустить систему
```
2. Создать и выполнить скрипт 1_ssh_keygen.sh
```
vim 1_ssh_keygen.sh
sudo chmod +x 1_ssh_keygen.sh
sudo ./1_ssh_keygen.sh
```
3. Создать и выполнить скрипт 2_clone_project.sh
```
vim 2_clone_project.sh
sudo chmod +x 2_clone_project.sh
sudo ./2_clone_project.sh
```
4. Установить NCALayer
```
Установить NCALayer из офф сайта.
Проверить модуль гос закупок на этих сайтах: https://mhelp.kz/ncalayer-skachat/#google_vignette, https://pki.gov.kz/docs/nl_ru/bundles/#_2
Всегда надо использовать последнюю версию.
Скопировать kz.ecc.NurSignBundle_5.1.1_2e62beae-e900-4c8c-9d8e-37286ace46ec.jar в конфиг:  
cp kz.ecc.NurSignBundle_5.1.1_2e62beae-e900-4c8c-9d8e-37286ace46ec.jar /home/asus/.config/NCALayer/bundles  
После перезапуска модуль должен исчезнуть из папку bundles  

Настроить автозапуск либо через скрипт либо через окружение
cd /projects/goszakup/sh/ncalayer
./4_ncalayer_config.sh

Если есть ошибка на xdd, то установить
sudo apt install xdd -y
```
6. Установить Docker
```
cd /projects/goszakup/sh
./6_docker_install.sh
```

7. Запустить сервисы из docker compose 
```
cd /projects/goszakup/sh
./7_compose_start.sh

```
8. Установить webdriver
```
cd /projects/goszakup/sh
./8_chromedriver.sh
```
9. Настроить зависимости
```
cd /projects/goszakup/sh
./9_setup_venv.sh
```
10. Создать env для сервиса Goszakup
```
cd /projects/goszakup/sh
./10_goszakup_env.sh
```
11. Настроить автозапуск сервиса Goszakup
```
cd /projects/goszakup/sh
./13_setup_goszakup.sh
```
12. Перезапустит систему
```
sudo reboot
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
