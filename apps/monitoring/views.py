from django.db.models import Avg
from rest_framework import viewsets
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UptimeRecord
from .serializers import (
    IntervalScheduleSerializer,
    PeriodicTaskSerializer,
    UptimeRecordSerializer,
)
from .statistics import QUERY_TIME_RANGE_TYPE, calculate_past


class IntervalScheduleViewSet(viewsets.ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer


class PeriodicTaskViewSet(viewsets.ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer


class UptimeRecordViewSet(viewsets.ModelViewSet):
    queryset = UptimeRecord.objects.all()
    serializer_class = UptimeRecordSerializer

    @action(detail=False, methods=["get"])
    def stats(self, request):
        service_id = request.query_params.get("service_id")
        time_range = int(request.query_params.get("time_range", 1))

        if service_id:
            queryset = UptimeRecord.objects.filter(service_id=service_id)
        else:
            queryset = self.get_queryset()

        # Apply time_range if specified and valid
        if time_range in QUERY_TIME_RANGE_TYPE:
            total_records, uptime_percentage, average_response_time = calculate_past(
                time_range=time_range
            )
        else:
            # Calculate for all time if time_range not specified or invalid
            total_records = queryset.count()
            up_records = queryset.filter(status=True).count()
            uptime_percentage = (
                (up_records / total_records) * 100 if total_records else 0
            )
            average_response_time = (
                queryset.filter(status=True).aggregate(Avg("response_time"))[
                    "response_time__avg"
                ]
                or 0
            )

        data = {
            "total_records": total_records,
            "uptime_percentage": uptime_percentage,
            "average_response_time": average_response_time,
        }

        return Response(data)
