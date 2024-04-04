import pytest
from dj_rest_auth.tests.mixins import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from apps.monitoring.models import UptimeRecord
from apps.monitoring.serializers import PeriodicTaskSerializer
from apps.notification.models import NotificationChannel, NotificationType
from apps.service.models import Service


@pytest.fixture
def api_client():
    return APIClient()


# Setup a fixture for the notification channel that can be used across multiple tests
@pytest.fixture
def notification_channel(db):
    return NotificationChannel.objects.create(
        name="Test Channel",
        type=NotificationType.BARK,
        details={"url": "https://bark.example.com"},
    )


@pytest.fixture
def test_service(db):
    return Service.objects.create(
        name="Test Service",
        description="A test service.",
        monitoring_endpoint="http://127.0.0.1",
        is_active=True,
    )


@pytest.fixture
def test_uptime_record(db, test_service):
    return UptimeRecord.objects.create(
        service=test_service,
        status=True,
        response_time=100.0,
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


def test_create_valid_uptime_record(test_uptime_record):
    """Test uptime record creation with valid data."""
    assert test_uptime_record.status
    assert test_uptime_record.response_time == 100.0
    assert test_uptime_record.error_message is None


def test_uptime_record_list(api_client, test_uptime_record):
    """
    Test fetching the list of uptime records.
    """
    response = api_client.get("/uptime/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


def test_filter_uptime_records_by_service(api_client, test_service, test_uptime_record):
    """
    Test filtering uptime records by service.
    """
    response = api_client.get(f"/uptime/?service_id={test_service.id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["service"] == test_service.id


def test_uptime_record_creation(api_client, test_service):
    """
    Test creating a new uptime record.
    """
    response = api_client.post(
        "/uptime/",
        {
            "service": test_service.id,
            "status": True,
            "response_time": 50.0,
        },
    )

    response = api_client.post(
        "/uptime/",
        {
            "service": test_service.id,
            "status": True,
            "response_time": 150.0,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert UptimeRecord.objects.count() == 2
    assert UptimeRecord.objects.first().service == test_service
    response = api_client.get(f"/uptime/?service_id={test_service.id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
