from django.db import models
from apps.service.models import Service

all_channels = {
    "bark": "Bark",
    "email": "Email",
    "telegram": "Telegram",
}


class NotificationChannel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    details = models.JSONField()
    type = models.TextChoices(
        "NotificationType", [(k, v) for k, v in all_channels.items()]
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
