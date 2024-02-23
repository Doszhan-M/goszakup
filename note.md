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


на fastapi.
команда запуска такая: uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 2
директория из которой надо ее выполнить: /projects/goszakup/goszakup
программа должна автозапускаться после перезагрузки системы
должно использоваться venv, который находиться по пути: /projects/goszakup/venv

надо чтобы перед стартом программы создавался файл .env c содержимым:
HEADLESS_DRIVER=TRUE
ENVIRONMENT=LXDE


надо создать скрипт, который создает systemd задачу для запуска приложения ncalayer.
команда запуска такая:  ./ncalayer.sh --restart 
директория из которой надо ее выполнить: ~/Programs/NCALayer/
программа должна автозапускаться после перезагрузки системы