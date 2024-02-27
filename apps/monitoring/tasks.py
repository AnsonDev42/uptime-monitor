from celery import shared_task
from .models import Service
from apps.notification.models import NotificationChannel, NotificationLog
from .utils import check_service_status


@shared_task
def check_all_services_status():
    for service in Service.objects.all():
        is_up, response_time = check_service_status(service.monitoring_endpoint)
        if not is_up:
            message = f"Service {service.name} is down."
            channels = NotificationChannel.objects.all()  # Example: Notify all channels
            for channel in channels:
                was_success = channel.send_notification(service, message)
                NotificationLog.objects.create(
                    service=service, message=message, was_success=was_success
                )
