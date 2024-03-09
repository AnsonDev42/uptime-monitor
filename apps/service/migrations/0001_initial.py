# Generated by Django 5.0.2 on 2024-03-08 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("notification", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
                ("monitoring_endpoint", models.URLField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "monitoring_type",
                    models.CharField(
                        choices=[("http", "HTTP"), ("ping", "PING")],
                        default="http",
                        max_length=50,
                    ),
                ),
                (
                    "notification_channel",
                    models.ManyToManyField(
                        blank=True, to="notification.notificationchannel"
                    ),
                ),
            ],
        ),
    ]
