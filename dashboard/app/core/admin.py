from django.contrib import admin


class MyAdminSite(admin.AdminSite):
    """Переопределить базовый админ сайт."""

    site_header = "Госзакуп"
    site_title = "Goszakup"
    index_title = "Goszakup"
