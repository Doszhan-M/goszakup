1. Доступные действия - Создать заявку 
2. Юридический адрес -- 050061  
3. ИИК -- Банк: АО "ForteBank" ИИК: KZ5696502F0017154550 БИК: IRTYKZKA 
4. Приложение 1-1 к Правилам осуществления государственных закупок с применением особого порядка   
5. сформировать документ -Ю подписать через rsa
6. вернуться к списку
7. далее - подать заявку - да
8. Статус заявки - Подана                         

941140001504
021240015299
120540009382

https://v3bl.goszakup.gov.kz/ru/application/create/11608950

https://v3bl.goszakup.gov.kz/ru/announce/index/11703621


django-admin startproject core
python manage.py migrate
python manage.py startapp dashboard
python manage.py runserver 0.0.0.0:8080
gunicorn --workers=1 --threads=2 dashboard.wsgi --bind 0.0.0.0:80 --log-level=info --access-logfile '-' --error-logfile '-' --access-logformat "%(m)s: %(U)s - %(s)s" --reload
