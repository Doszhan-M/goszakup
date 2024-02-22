1. Доступные действия - Создать заявку 
2. Юридический адрес -- 050061  
3. ИИК -- Банк: АО "ForteBank" ИИК: KZ5696502F0017154550 БИК: IRTYKZKA 
4. Приложение 1-1 к Правилам осуществления государственных закупок с применением особого порядка   
5. сформировать документ -Ю подписать через rsa
6. вернуться к списку
7. далее - подать заявку - да
8. Статус заявки - Подана                         



sudo mkdir projects
sudo chmod -R 777 /projects
sudo setfacl -m d:u::rwx /projects
sudo setfacl -m d:g::rwx /projects
sudo setfacl -m d:o::rwx /projects
cd /projects
git clone git@github.com:Doszhan-M/goszakup.git
cd /goszakup
