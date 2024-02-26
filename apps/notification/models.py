import httpx
from django.db import models
from apps.service.models import Service


class NotificationChannel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    details = models.JSONField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def send_notification(self, service, message):
        raise NotImplementedError("Method not implemented")


class BarkChannel(NotificationChannel):
    endpoint = models.URLField(max_length=255, default="https://api.day.app")

    def send_notification(self, service, message):
        prepared_message = f"{service.name} - {message}"
        # Send the notification to the bark server
        # get the response and return it
        with httpx.Client(http2=True) as client:
            response = client.post(
                f"{self.endpoint}/UptimeMonitor alert/{prepared_message}",
                headers=self._headers,
                json=message,
            )
            if not response.is_success:
                return False
            return True


class NotificationLog(models.Model):
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField("Notification Message", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    was_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.channel.name} - {self.created_at}"
