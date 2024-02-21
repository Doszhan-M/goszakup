from django.utils import timezone
from django.db.models import (
    Model,
    CASCADE,
    TextField,
    CharField,
    FileField,
    ForeignKey,
    DateTimeField,
    TextChoices,
    DurationField,
)


def eds_directory_path(instance, filename):
    return "eds/{0}/{1}".format(instance.iin_bin, filename)


class Participant(Model):

    iin_bin = CharField(
        max_length=255,
        default="141140001428",
        verbose_name="ИИН/БИН участника",
        unique=True,
    )
    name = CharField(
        max_length=255,
        default="ТОО 'Сивер плюс'",
        verbose_name="Наименование участника",
    )
    eds_auth = FileField(
        upload_to=eds_directory_path, verbose_name="ЭЦП для авторизации"
    )
    eds_gos = FileField(upload_to=eds_directory_path, verbose_name="ЭЦП для подписания")
    eds_pass = CharField(max_length=255, verbose_name="Пароль от ЭЦП")
    goszakup_pass = CharField(max_length=255, verbose_name="Пароль на сайте Госзакупа")
    subject_address = CharField(
        max_length=255,
        default="050061",
        verbose_name="Индекс",
        help_text="Необходимо ввести индекс, который зарегистрирован на сайте",
    )
    iik = CharField(
        max_length=255,
        default="KZ5696502F0017154550",
        verbose_name="Счет для оплаты",
        help_text="Необходимо ввести счет, который зарегистрирован на сайте",
    )
    contact_phone = CharField(
        max_length=255,
        default="7014333488",
        verbose_name="Номер телефона",
        help_text="Необходимо ввести номер, который зарегистрирован на сайте, вводить без 8 или +7. Пример: 7014333488",
    )

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        db_table = "participant"

    def __str__(self):
        return self.name


class Status(TextChoices):
    checking = "checking", "Проверка объявления"
    pending = "pending", "В ожидании"
    in_progress = "in_progress", "В процессе"
    success = "success", "Завершено успешно!"
    error = "error", "Завершено с ошибкой!"


class Task(Model):
    announce_number = CharField(
        max_length=256,
        verbose_name="Номер объявления",
        unique=True,
    )
    status = CharField(
        max_length=256,
        choices=Status.choices,
        default=Status.checking,
        verbose_name="Статус",
    )
    create_time = DateTimeField(
        default=timezone.now,
        verbose_name="Время создания",
    )
    company = ForeignKey(
        Participant,
        on_delete=CASCADE,
        verbose_name="Участник",
    )
    user = ForeignKey(
        "auth.User",
        on_delete=CASCADE,
        verbose_name="Пользователь",
    )
    scheduled_time = DateTimeField(
        blank=True,
        null=True,
        verbose_name="Запланированное время старта",
    )
    start_time = DateTimeField(
        blank=True,
        null=True,
        verbose_name="Время старта",
    )
    finish_time = DateTimeField(
        blank=True,
        null=True,
        verbose_name="Время завершения",
    )
    duration = DurationField(
        blank=True,
        null=True,
        verbose_name="Продолжительность выполнения",
    )
    error = TextField(
        blank=True,
        null=True,
        verbose_name="Описание ошибки",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        db_table = "task"

    def __str__(self):
        return self.announce_number
