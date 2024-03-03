from rest_framework import serializers
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from apps.monitoring.models import UptimeRecord


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"


class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = "__all__"


class UptimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UptimeRecord
        fields = "__all__"
