from celery import shared_task
from .models import Service, UptimeRecord
from apps.notification.models import NotificationChannel, NotificationLog
from .utils import check_service_status
# logger = get_task_logger(__nae__)
# logger_django = logging.getLogger(__name__)


@shared_task
def check_all_services_status():
    # log the status of all services
    # breakpoint()
    # logger.inf("Checking all services status")
    # logger_django.info("Checking all services status")
    for service in Service.objects.all():
        is_up, response_time, error_message = check_service_status(
            service.monitoring_endpoint
        )
        UptimeRecord.objects.create(
            status=is_up, response_time=response_time, error_message=error_message
        )

        if not is_up:
            message = f"Service {service.name} is down."
            channels = NotificationChannel.objects.all()  # Example: Notify all channels
            for channel in channels:
                was_success = channel.send_notification(service, message)
                NotificationLog.objects.create(
                    service=service, message=message, was_success=was_success
                )
        else:
            message = f"Service {service.name} is up."
            channels = NotificationChannel.objects.all()  # Example: Notify all channels
            for channel in channels:
                was_success = channel.send_notification(service, message)
                NotificationLog.objects.create(
                    service=service, message=message, was_success=was_success
                )
