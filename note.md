python manage.py makemigrations
python manage.py migrate


watchfiles --filter python 'celery -A core worker -Q beat_tasks -B --pool=prefork --concurrency=4 --max-tasks-per-child=1'
