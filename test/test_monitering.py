import pytest
from rest_framework.exceptions import ErrorDetail

from apps.monitoring.serializers import PeriodicTaskSerializer
from apps.notification.models import NotificationChannel, NotificationType


# Setup a fixture for the notification channel that can be used across multiple tests
@pytest.fixture
def notification_channel(db):
    return NotificationChannel.objects.create(
        name="Test Channel",
        type=NotificationType.BARK,
        details={"url": "https://bark.example.com"},
    )


@pytest.mark.django_db
def test_create_valid_periodic_task_data(notification_channel):
    """Test service creation with valid periodic_task data."""
    data = {
        "name": "Test Task 111",
        "task": "apps.monitoring.tasks.check_monitor_services_status",
        "kwargs": {},
        "interval": {
            "every": 10,
            "period": "seconds",
        },
        "enabled": True,
    }
    serializer = PeriodicTaskSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_create_invalid_periodic_task_data_missing_every(notification_channel):
    """Test service creation with invalid periodic_task data."""
    data = {
        "name": "Test Task 111",
        "task": "apps.monitoring.tasks.check_monitor_services_status",
        "kwargs": {},
        "interval": {
            "period": "seconds",
        },
        "enabled": True,
    }
    serializer = PeriodicTaskSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors == {
        "interval": {
            "every": [ErrorDetail(string="This field is required.", code="required")]
        }
    }


def test_create_invalid_periodic_task_data_missing_period(notification_channel):
    """Test service creation with invalid periodic_task data."""
    data = {
        "name": "Test Task 111",
        "task": "apps.monitoring.tasks.check_monitor_services_status",
        "kwargs": {},
        "interval": {
            "every": 10,
        },
        "enabled": True,
    }
    serializer = PeriodicTaskSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors == {
        "interval": {
            "period": [ErrorDetail(string="This field is required.", code="required")]
        }
    }


def test_create_invalid_periodic_task_data_missing_interval(notification_channel):
    """Test service creation with invalid periodic_task data."""
    data = {
        "name": "Test Task 111",
        "task": "apps.monitoring.tasks.check_monitor_services_status",
        "kwargs": {},
        "enabled": True,
    }
    serializer = PeriodicTaskSerializer(data=data)
    assert not serializer.is_valid()
    assert serializer.errors == {
        "interval": [ErrorDetail(string="This field is required.", code="required")]
    }
