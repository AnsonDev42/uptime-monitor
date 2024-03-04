# Generated by Django 5.0.2 on 2024-03-03 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_celery_beat", "0018_improve_crontab_helptext"),
        ("service", "0002_service_monitoring_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="periodic_task",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="django_celery_beat.periodictask",
            ),
        ),
    ]
