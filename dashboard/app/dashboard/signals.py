from datetime import datetime, timedelta

from django.conf import settings
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
        hasattr(instance, "_suppress_schedule_announce")
        and instance._suppress_schedule_announce
    ):
        return
    if instance.status in ("checking",):
        announce_id= instance.id
        participant_id = instance.participant.id
        scheduled_time = settings.ALMATY_TZ.localize(
            datetime.now() + timedelta(seconds=2)
        )
        announce.check_and_schedule_task.apply_async(
            args=(announce_id, participant_id),
            eta=scheduled_time,
        )
