python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate

admin:aCiOnIQuArdE

gunicorn --workers=1 --threads=2 core.wsgi --bind 0.0.0.0:8080 --log-level=info --access-logfile '-' --error-logfile '-' --access-logformat "%(m)s: %(U)s - %(s)s" --reload

watchfiles --filter python 'celery -A core worker -Q beat_tasks -B --pool=prefork --concurrency=4 --max-tasks-per-child=1'

941140001504
021240015299
120540009382

https://v3bl.goszakup.gov.kz/ru/application/create/11695620
https://v3bl.goszakup.gov.kz/ru/announce/index/11695620