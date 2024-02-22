import pytz
from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Task
from .tasks import announce


@receiver(post_save, sender=Task)
def schedule_announce(
    sender: Task, instance: Task, created, update_fields, *args, **kwargs
) -> None:
    """Запланировать задачу."""

    if (
        hasattr(instance, "_suppress_post_save_signal")
        and instance._suppress_post_save_signal
    ):
        return
    if (
        instance.last_check_time is None
        or timezone.now() - instance.last_check_time > timedelta(minutes=5)
        and not instance.scheduled_time
    ):
        announce_number = instance.announce_number
        participant_id = instance.participant.id
        almaty_tz = pytz.timezone("Asia/Almaty")
        scheduled_time = almaty_tz.localize(datetime.now() + timedelta(seconds=2))
        announce.check_and_schedule_task.apply_async(
            args=(
                announce_number,
                participant_id,
            ),
            eta=scheduled_time,
        )
