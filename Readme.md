# Install and Start
1. Настроить debian lxde:
```
su -  
apt update && apt upgrade -y  
apt install sudo  
usermod -aG sudo linux  
reboot  

sudo apt update && sudo apt upgrade -y  
sudo apt -y install htop vim curl wget libnss3-tools unzip
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
cd /projects/goszakup/sh/ncalayer
Настроить автозапуск либо через скрипт либо через окружение
./4_ncalayer_config.sh
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
