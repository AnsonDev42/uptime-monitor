from rest_framework import viewsets
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from .serializers import IntervalScheduleSerializer, PeriodicTaskSerializer


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
