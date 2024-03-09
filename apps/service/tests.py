from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.monitoring.serializers import PeriodicTaskSerializer
from apps.notification.models import NotificationChannel, NotificationType
from apps.service.serializers import ServiceSerializer


class ServiceSerializerValidationTest(TestCase):
    def test_validation_both_fields_provided(self):
        """Test that ValidationError is raised when both periodic_task_id and periodic_task are provided."""
        data = {
            "periodic_task_id": 1,
            "periodic_task": {"name": "Test Task", "interval": "daily"},
            # include other necessary fields for serializer
        }
        serializer = ServiceSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validation_no_fields_provided(self):
        """Test that ValidationError is raised when neither periodic_task_id nor periodic_task are provided."""
        data = {
            # include other necessary fields for serializer
        }
        serializer = ServiceSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    # Add more tests for other validation rules...


class ServiceSerializerCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup necessary data for tests, like creating PeriodicTasks and NotificationChannels
        cls.periodic_task_data = {
            "name": "Test Task",
            "task": "apps.monitoring.tasks.check_monitor_services_status",
            # "kwargs":'{"service_id": 1}',
            "interval": {
                "every": 10,
                "period": "seconds",
            },
            "enabled": True,
        }
        cls.notification_channel = NotificationChannel.objects.create(
            name="Test Channel",
            type=NotificationType.BARK,
            details={"url": "https://bark.example.com"},
        )
        cls.notification_channel.save()

    def test_create_service_with_periodic_task_data(self):
        """Test service creation with periodic_task data."""
        # periodic_task_serializer = PeriodicTaskSerializer(instance=self.periodic_task)

        periodic_task_serializer = PeriodicTaskSerializer(data=self.periodic_task_data)
        self.assertTrue(
            periodic_task_serializer.is_valid(), periodic_task_serializer.errors
        )
        data = {
            "name": "test b",
            "description": "test",
            "monitoring_endpoint": "http://localhost:8000/service/",
            "is_active": True,
            "notification_channel": [],
            "monitoring_type": "http",
            "periodic_task_data": self.periodic_task_data,
        }
        serializer = ServiceSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        service = serializer.save()
        self.assertIsNotNone(service.periodic_task)
        self.assertEqual(service.periodic_task.name, "Test Task")

    def test_create_service_with_notification_id(self):
        """Test service creation with a_notification_id."""
        data = {
            "name": "brruno",
            "description": "test",
            "monitoring_endpoint": "http://localhost:8000/service/",
            "is_active": True,
            "notification_channel": [self.notification_channel.id],
            "monitoring_type": "http",
            "periodic_task_data": self.periodic_task_data,
        }

        self.assertTrue(
            isinstance(self.notification_channel.id, int),
            "Notification channel id is not an integer",
        )
        serializer = ServiceSerializer(data=data)
        print(data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        service = serializer.save()
        self.assertEqual(
            service.notification_channel.first().id, self.notification_channel.id
        )

    def test_create_service_with_null_periodic_task_data(self):
        """Test service creation with null periodic_task data."""
        data = {
            "name": "test b",
            "description": "test",
            "monitoring_endpoint": "http://localhost:8000/service/",
            "is_active": True,
            "notification_channel": [],
            "monitoring_type": "http",
            "periodic_task_data": None,
        }
        serializer = ServiceSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        service = serializer.save()
        self.assertIsNone(service.periodic_task)
        self.assertEqual(service.name, "test b")

    def test_create_service_with_invalid_periodic_task_data(self):
        data = {
            "name": "test b",
            "description": "test",
            "monitoring_endpoint": "http://localhost:8000/service/",
            "is_active": True,
            "notification_channel": [],
            "monitoring_type": "http",
            "periodic_task_data": {"name": "Test Task", "interval": "daily"},
        }

        serializer = ServiceSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("every", serializer.errors)
