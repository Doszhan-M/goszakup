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
        "duration",
        "participant",
    )
    search_fields = ("announce_number",)
    list_filter = ("status",)
    ordering = ("-scheduled_time",)
    readonly_fields = (
        "scheduled_time",
        "start_time",
        "finish_time",
        "duration",
        "create_time",
        "status",
        "error",
        "announce_name",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields["user"].initial = request.user
        return form


class ParticipantDash(BaseAdmin):
    list_display = ("name", "iin_bin")
    search_fields = ("name", "iin_bin")


admin.site.register(Task, TaskDash)
admin.site.register(Participant, ParticipantDash)
