from django.db import models


class monitoring_type(models.TextChoices):
    HTTP = "http", "HTTP"
    PING = "ping", "PING"


class Service(models.Model):
    """
    Service model stores all the details of a monitor service that is being created.
    It is the foreign key for the UptimeRecord model
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    monitoring_endpoint = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    notification_channel = models.ManyToManyField(
        "notification.NotificationChannel", blank=True
    )
    monitoring_type = models.CharField(
        max_length=50, default="http", choices=monitoring_type.choices
    )

    def __str__(self):
        return self.name
