from django.db import models
from apps.service.models import Service


class UptimeRecord(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    response_time = models.FloatField(null=True, blank=True)
    check_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {'Up' if self.status else 'Down'} at {self.checked_at}"
