
## Для установки Pritunl на сервер Debian 11:
```
sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list << EOF
deb https://repo.mongodb.org/apt/debian buster/mongodb-org/6.0 main
EOF

sudo tee /etc/apt/sources.list.d/pritunl.list << EOF
deb https://repo.pritunl.com/stable/apt buster main
EOF

sudo apt --assume-yes install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com --recv 7568D9BB55FF9E5287D586017AE645C0CF8E292A
sudo apt update
sudo apt --assume-yes install pritunl mongodb-org
sudo systemctl start mongod pritunl
sudo systemctl enable mongod pritunl
sudo systemctl status pritunl
```

## Если есть ошибка с libffi.so.6

### 1.Установите необходимые пакеты:
```
sudo apt install libffi7
```
### 2.Создайте символическую ссылку для libffi.so.6:
```
sudo ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libffi.so.6
```
### 3.Перезапустите сервис Pritunl:
```
sudo systemctl restart pritunl
sudo systemctl status pritunl
```

## Конфигурация Pritunl

[Зайти на админ панель](https://195.49.210.241/setup)   

### Получить первичный ключ:
```
sudo pritunl setup-key
```

debian@195.49.210.241  
pritunl_admin:AnewingSitHeigNIZaREstoNeisEAtIonJ  
