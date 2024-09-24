import requests

from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime

from core.celery import app
from core.config import setup
from dashboard.models import Task


@app.task(acks_late=True, queue="beat_tasks")
def start_tender(announce_id, data):
    """Начать тендер."""

    task = Task.objects.get(id=announce_id)
    url = (
        f"{setup.GOSZAKUP_URL}/goszakup/tender_start/?announce_number={task.announce_number}"
    )
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, data=data, timeout=9600)
    status_code = response.status_code
    result: dict = response.json()
    if status_code == 200 and result.get("success"):
        task.start_time = make_aware(parse_datetime(result["start_time"]))
        task.finish_time = make_aware(parse_datetime(result["finish_time"]))
        task.duration = result["duration"]
        task.status = "success"
    elif status_code == 200 and not result.get("success"):
        task.start_time = make_aware(parse_datetime(result["start_time"]))
        task.finish_time = make_aware(parse_datetime(result["finish_time"]))
        task.duration = result["duration"]        
        task.error = result["error_text"]
        task.status = "error"
    elif status_code == 500 and result.get("detail"):
        task.status = "error"
        task.error = result["detail"]["description"]
    elif status_code == 500:
        task.status = "error"
        task.error = str(result)
    else:
        task.status = "error"
        task.error = "Неизвестная ошибка"
    task._suppress_schedule_announce = True
    task.save()
    return task.status
