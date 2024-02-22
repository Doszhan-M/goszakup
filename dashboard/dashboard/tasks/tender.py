import requests

from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime

from core.celery import app
from dashboard.models import Task


@app.task(acks_late=True, queue="beat_tasks")
def start_tender(announce_number, data):
    """Начать тендер."""

    url = f"http://127.0.0.1:8000/goszakup/tender_start/?announce_number={announce_number}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=data, timeout=9600)
    task = Task.objects.get(announce_number=announce_number)
    if response.status_code == 200 and response.json()["success"]:
        result = response.json()
        task.start_time = make_aware(parse_datetime(result["start_time"]))
        task.finish_time = make_aware(parse_datetime(result["finish_time"]))
        task.duration = result["duration"]
        task.status = "success"
    elif response.status_code == 500:
        task.status = "error"
        task.error = "Статус ошибки 500"
    elif response.status_code == 200 and not response.json()["success"]:
        task.status = "error"
        task.error = response.json()["error_text"]
    else:
        task.status = "error"
        task.error = "Неизвестная ошибка"
    task.save()
    return task.status
