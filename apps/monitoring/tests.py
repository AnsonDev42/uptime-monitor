from django.test import TestCase
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from apps.monitoring.serializers import (
    IntervalScheduleSerializer,
    PeriodicTaskSerializer,
)


class IntervalScheduleSerializerTest(TestCase):
    def test_valid_serializer(self):
        valid_data = {
            "every": 10,  # Assuming `every` is a field of IntervalSchedule
            "period": "seconds",  # Assuming `period` is a field of IntervalSchedule
        }
        serializer = IntervalScheduleSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        invalid_data = {
            "every": -10,  # Invalid if negative values are not allowed
            # Missing `period` field
        }
        serializer = IntervalScheduleSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class PeriodicTaskSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup required for all tests
        cls.interval = IntervalSchedule.objects.create(
            every=10, period=IntervalSchedule.SECONDS
        )

    def test_valid_serializer(self):
        valid_data = {
            "name": "Test Task",
            "task": "apps.monitoring.tasks.check_monitor_services_status",
            "kwargs": '{"service_id": 1}',
            "interval": {
                "every": 10,
                "period": "seconds",
            },
            "enabled": True,
        }
        serializer = PeriodicTaskSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        # Test object creation
        periodic_task = serializer.save()
        self.assertIsInstance(periodic_task, PeriodicTask)
        self.assertEqual(periodic_task.interval.every, self.interval.every)
        self.assertEqual(periodic_task.interval.period, self.interval.period)

    def test_valid_serializer_data_null_periodic_task(self):
        # Similar to the above, but provide invalid data and assert serializer.is_valid() is False
        pass
