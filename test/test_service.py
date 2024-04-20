import pytest
from rest_framework.exceptions import ValidationError

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
def test_validation_both_fields_provided():
    """Test that ValidationError is raised when both periodic_task_id and periodic_task are provided."""
    data = {
        "periodic_task_id": 1,
        "periodic_task": {"name": "Test Task", "interval": "daily"},
        # include other necessary fields for serializer
    }
    serializer = ServiceSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_validation_no_fields_provided():
    """Test that ValidationError is raised when neither periodic_task_id nor periodic_task are provided."""
    data = {
        # include other necessary fields for serializer
    }
    serializer = ServiceSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_service_with_periodic_task_data(periodic_task_data):
    """Test service creation with periodic_task data."""
    data = {
        "name": "test b",
        "description": "test",
        "monitoring_endpoint": "http://localhost:8000/service/",
        "is_active": True,
        "notification_channel": [],
        "monitoring_type": "http",
        "periodic_task_data": periodic_task_data,
    }
    serializer = ServiceSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    service = serializer.save()
    assert service.periodic_task is not None
    assert data["name"] in service.periodic_task.name
    assert (
        service.periodic_task.interval.every == 10
    ), service.periodic_task.interval.every
    assert service.periodic_task.interval.period == "seconds"


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
