from django.db import models
from apps.service.models import Service


class NotificationType(models.TextChoices):
    TELEGRAM = "telegram", "Telegram"
    BARK = "bark", "Bark"


class NotificationChannel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    details = models.JSONField()
    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.BARK,
    )

    def __str__(self):
        return self.name

    def send_notification(self, service, message):
        if self.type == "telegram":
            from apps.notification.notify_services.telegram import Telegram

            telegram = Telegram(**self.details)
            return telegram.send_notification(service, message)
        elif self.type == "bark":
            from apps.notification.notify_services.bark import Bark

            bark = Bark(**self.details)
            return bark.send_notification(service, message)


class NotificationLog(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField("Notification Message", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    was_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.channel.name} - {self.created_at}"
