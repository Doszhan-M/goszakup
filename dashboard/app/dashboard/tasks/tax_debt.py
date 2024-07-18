import json
import time
import requests

from django.conf import settings

from core.celery import app
from dashboard.models import Participant


@app.task(acks_late=True, queue="beat_tasks")
def check_tax_debt():
    """Проверить налоговые долги участников."""

    url = f"{settings.GOSZAKUP_URL}/goszakup/check_tax_debt/?delta=10"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    all_participants = Participant.objects.all()
    for participant in all_participants:
        data = json.dumps(
            {
                "eds_gos": participant.eds_gos_path,
                "eds_pass": participant.eds_pass,
                "goszakup_pass": participant.goszakup_pass,
            }
        )
        retry_count = 0
        max_retries = 3
        success = False
        while retry_count < max_retries and not success:
            response = requests.post(url, headers=headers, data=data, timeout=300)
            if response.status_code == 200:
                success = True
            else:
                retry_count += 1
                time.sleep(3)
        if not success:
            print(f"Failed to check tax debt for participant: {participant}")
        return {"success": success}
