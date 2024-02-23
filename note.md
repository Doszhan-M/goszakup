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


сейчас я запускаю программу на fastapi таким скриптом start_project.sh:
#!/bin/bash
# Запускаем GNOME Terminal и выполняем в нем run_app.sh
gnome-terminal -- /bin/bash -c './11_start_goszakup.sh; exec bash'

содержимое скрипта 11_start_goszakup.sh такое:
#!/bin/bash
source /projects/goszakup/venv/bin/activate
cd /projects/goszakup/goszakup
nohup uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --workers 1 &

надо создать скрипт, который создаст systemd задачу для запуска скрипта start_project.sh
который в свою очередь запустить 11_start_goszakup.sh

[Desktop Entry]
Type=Application
Name=Goszakup
Exec=/projects/goszakup/sh/12_launch_goszakup.sh
Terminal=false
