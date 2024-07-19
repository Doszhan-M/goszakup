# Generated by Django 5.0.7 on 2024-07-18 06:07

import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='eds_auth',
        ),
        migrations.AlterField(
            model_name='participant',
            name='eds_gos',
            field=models.FileField(upload_to=dashboard.models.eds_directory_path, verbose_name='ЭЦП файл'),
        ),
    ]