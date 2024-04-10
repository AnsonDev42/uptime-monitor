import pytest

from apps.notification.models import NotificationChannel, NotificationType
from apps.service.serializers import ServiceSerializer


# Setup a fixture for the notification channel that can be used across multiple tests
@pytest.fixture
def notification_channel(db):
    return NotificationChannel.objects.create(
        name="Test Channel",
        type=NotificationType.BARK,
        details={"url": "https://bark.example.com"},
    )


# Setup a fixture for the periodic task data
@pytest.fixture
def periodic_task_data():
    return {
        "name": "Test Task",
        "task": "apps.monitoring.tasks.check_monitor_services_status",
        # "kwargs": {},
        "interval": {
            "every": 10,
            "period": "seconds",
        },
        "enabled": True,
    }


@pytest.mark.django_db
def test_create_service_with_notification_id(notification_channel, periodic_task_data):
    """Test service creation with a_notification_id."""
    data = {
        "name": "brruno",
        "description": "test",
        "monitoring_endpoint": "http://localhost:8000/service/",
        "is_active": True,
        "notification_channel": [notification_channel.id],
        "monitoring_type": "http",
        "periodic_task_data": periodic_task_data,
    }

    assert isinstance(
        notification_channel.id, int
    ), "Notification channel id is not an integer"
    serializer = ServiceSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    service = serializer.save()
    assert service.notification_channel.first().id == notification_channel.id
