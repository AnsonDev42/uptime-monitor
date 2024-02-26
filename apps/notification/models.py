from django.db import models
from apps.service.models import Service


class NotificationChannel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    details = models.JSONField()

    def __str__(self):
        return self.name


class NotificationLog(models.Model):
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField("Notification Message", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    was_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.channel.name} - {self.created_at}"
