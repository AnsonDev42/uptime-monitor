from celery import shared_task
from apps.monitoring.models import Service, UptimeRecord
from apps.notification.models import NotificationChannel, NotificationLog
from apps.monitoring.utils import check_service_status


# logger = get_task_logger(__nae__)
# logger_django = logging.getLogger(__name__)
# @celery_app.on_after_configure.connect


@shared_task
def check_monitor_services_status(service_id=None):
    if (
        service_id is None
        or service_id == ""
        or not Service.objects.filter(id=service_id).exists()
    ):
        return
    service = Service.objects.get(id=service_id)
    if not service.is_active:
        return
    is_up, response_time, error_message = check_service_status(
        service.monitoring_endpoint
    )
    UptimeRecord.objects.create(
        status=is_up,
        response_time=response_time,
        error_message=error_message,
        service=service,
    )
    if not Service.objects.filter(id=service_id).exists():
        return
    if not is_up:
        message = f"Service {service.name} is down."
        channels = Service.objects.get(id=service_id).notification_channel.all()
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


if __name__ == "__main__":
    check_monitor_services_status(service_id=1)
    print("check_monitor_services_status()")
