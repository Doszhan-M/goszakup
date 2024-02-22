import json
import requests
from logging import getLogger
from datetime import timedelta, datetime

from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime

from core.celery import app
from dashboard.models import Participant, Task


logger = getLogger("django")


@app.task(acks_late=True, queue="beat_tasks")
def check_and_schedule_task(announce_number, participant_id):
    """Запланировать задачу."""

    url = f"http://127.0.0.1:8000/goszakup/tender_check/?announce_number={announce_number}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    participant = Participant.objects.get(id=participant_id)
    data = json.dumps(
        {
            "eds_auth": participant.eds_auth.path,
            "eds_gos": participant.eds_gos.path,
            "eds_pass": participant.eds_pass,
            "goszakup_pass": participant.goszakup_pass,
            "application_data": {
                "subject_address": participant.subject_address,
                "iik": participant.iik,
                "contact_phone": participant.contact_phone,
            },
        }
    )
    task = Task.objects.get(announce_number=announce_number)
    task._suppress_post_save_signal = True
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.post(url, headers=headers, data=data, timeout=60)
            if response.status_code == 200 and response.json()["success"]:
                break
            else:
                raise requests.exceptions.ReadTimeout
        except requests.exceptions.ReadTimeout:
            logger.error(f"Попытка {attempts + 1} не удалась: время ожидания истекло.")
            attempts += 1
            if attempts == max_attempts:
                logger.error("Достигнуто максимальное количество попыток.")
                task.status = "error"
                task.last_check_time = timezone.now()
                task.error = f"Не удалось запланировать задачу, попробуйте после {datetime.now() + timedelta(minutes=5)}"
                task.save()
                return
    announce_data = response.json()
    task.error = ""
    task.announce_name = announce_data["announce_name"]
    start_time = make_aware(parse_datetime(announce_data["start_time"]))
    task.scheduled_time = start_time - timedelta(minutes=5)
    finish_time = parse_datetime(announce_data["finish_time"])
    if finish_time < datetime.now():
        task.status = "success"
    else:
        task.status = "pending"
    task.save()
