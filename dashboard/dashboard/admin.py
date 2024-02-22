from django.contrib import admin

from .models import Participant, Task


class BaseAdmin(admin.ModelAdmin):

    menu_group = "Госзакуп"
    save_on_top = True
    list_per_page = 50


class TaskDash(BaseAdmin):
    list_display = (
        "announce_number",
        "status",
        "scheduled_time",
        "start_time",
        "finish_time",
        "duration",
    )
    search_fields = ("announce_number",)
    list_filter = ("status",)
    ordering = ("-create_time",)
    readonly_fields = (
        "scheduled_time",
        "start_time",
        "finish_time",
        "duration",
        "create_time",
        "status",
        "error",
        "announce_name",
        "last_check_time",
    )


class ParticipantDash(BaseAdmin):
    list_display = ("name", "iin_bin")
    search_fields = ("name", "iin_bin")


admin.site.register(Task, TaskDash)
admin.site.register(Participant, ParticipantDash)
