from os import environ

from celery import Celery
from celery.schedules import crontab


environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = "Asia/Almaty"
app.autodiscover_tasks()
