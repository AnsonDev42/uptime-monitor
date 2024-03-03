from rest_framework import viewsets
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import UptimeRecord
from .serializers import (
    IntervalScheduleSerializer,
    PeriodicTaskSerializer,
    UptimeRecordSerializer,
)


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer


class UptimeRecordViewSet(viewsets.ModelViewSet):
    queryset = UptimeRecord.objects.all()
    serializer_class = UptimeRecordSerializer
