import json
import requests
from logging import getLogger
from datetime import timedelta, datetime

from django.conf import settings
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime

from core.celery import app
from core.config import setup
from .tender import start_tender
from dashboard.models import Participant, Task


logger = getLogger("django")


@app.task(acks_late=True, queue="beat_tasks")
def check_and_schedule_task(announce_id, participant_id):
    """Запланировать задачу."""

    task = Task.objects.get(id=announce_id)
    url = (
        f"{setup.GOSZAKUP_URL}/goszakup/tender_check/?announce_number={task.announce_number}"
    )
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    participant = Participant.objects.get(id=participant_id)
    data = json.dumps(
        {
            "eds_gos": participant.eds_gos_path,
            "eds_pass": participant.eds_pass,
            "goszakup_pass": participant.goszakup_pass,
            "application_data": {
                "subject_address": participant.subject_address,
                "iik": participant.iik,
                "contact_phone": participant.contact_phone,
            },
        }
    )
    task._suppress_schedule_announce = True
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
                task.error = f"Не удалось запланировать задачу, попробуйте после {datetime.now() + timedelta(minutes=5)}"
                task.save()
                return
    announce_data = response.json()
    task.error = ""
    task.announce_name = announce_data["announce_name"]
    start_time = parse_datetime(announce_data["start_time"])
    task.scheduled_time = make_aware(start_time) - timedelta(minutes=5)
    finish_time = parse_datetime(announce_data["finish_time"])
    if finish_time < datetime.now():
        task.status = "success"
    elif start_time < datetime.now() and finish_time > datetime.now():
        task.status = "in_progress"
        scheduled_time = settings.ALMATY_TZ.localize(
            datetime.now() + timedelta(seconds=1)
        )
        start_tender.apply_async(
            args=(announce_id, data),
            eta=scheduled_time,
        )
    elif start_time > datetime.now():
        task.status = "pending"
        start_tender.apply_async(
            args=(announce_id, data),
            eta=task.scheduled_time,
        )
    task.save()
    return task.status
