from django.utils.timezone import now
from rest_framework import serializers
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from apps.monitoring.models import UptimeRecord


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"


choices = (
    (
        "apps.monitoring.tasks.check_monitor_services_status",
        "(HTTP GET) apps.monitoring.tasks.check_monitor_services_status",
    ),
    ("ping", "PING"),
)


class PeriodicTaskSerializer(serializers.ModelSerializer):
    task = serializers.ChoiceField(
        choices=choices,
    )
    interval = IntervalScheduleSerializer()
    kwargs = serializers.JSONField(default={"service_id": 1})

    class Meta:
        model = PeriodicTask
        fields = (
            "id",
            "name",
            "task",
            "kwargs",
            "one_off",
            "enabled",
            "last_run_at",
            "total_run_count",
            "date_changed",
            "description",
            "interval",
        )
        extra_kwargs = {
            "task": {
                "required": True,
                "default": "apps.monitoring.tasks.check_monitor_services_status",
            },
            "kwargs": {"required": False, "allow_null": True},
            "args": {"required": False},
            "exchange": {"required": False, "allow_null": True},
            "routing_key": {"required": False, "allow_null": True},
            "headers": {"required": False},
            "priority": {"required": False, "allow_null": True},
            "expires": {"required": False, "allow_null": True},
            "expire_seconds": {"required": False, "allow_null": True},
            "one_off": {"required": False},
            "enabled": {"required": False},
            "last_run_at": {"required": False, "read_only": True},
            "total_run_count": {"required": False, "read_only": True},
            "date_changed": {"required": False, "read_only": True},
            "description": {"required": False},
            "interval": {"required": True},
        }

    def create(self, validated_data):
        interval_data = validated_data.pop("interval")
        interval = IntervalSchedule.objects.create(**interval_data)
        start_time = now()
        periodic_task = PeriodicTask.objects.create(
            interval=interval, start_time=start_time, **validated_data
        )
        return periodic_task


class UptimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UptimeRecord
        fields = "__all__"
