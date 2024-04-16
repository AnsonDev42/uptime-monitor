from rest_framework import viewsets
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.monitoring.models import UptimeRecord
from apps.monitoring.serializers import (
    IntervalScheduleSerializer,
    PeriodicTaskSerializer,
    UptimeRecordSerializer,
)
from apps.monitoring.statistics import (
    QUERY_TIME_RANGE_TYPE,
    calculate_past_summary,
    calculate_past_chart,
    calculate_trackers_by_status,
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

    @action(detail=False, methods=["get"])
    def stats(self, request):
        time_range = int(request.query_params.get("time_range", 1))

        # Apply time_range if specified and valid
        if time_range not in QUERY_TIME_RANGE_TYPE:
            return Response({"error": "Invalid time range"}, status=400)
        (
            total_records,
            uptime_percentage,
            average_response_time,
        ) = calculate_past_summary(time_range=time_range)

        data = {
            "total_records": total_records,
            "uptime_percentage": uptime_percentage,
            "average_response_time": average_response_time,
        }

        return Response(data)

    @action(detail=False, methods=["get"])
    def chart(self, request):
        time_range = int(request.query_params.get("time_range", 1))
        split_interval = int(request.query_params.get("split_interval", 6))
        service_id = request.query_params.get("service_id")
        if time_range not in QUERY_TIME_RANGE_TYPE:
            return Response({"error": "Invalid time range"}, status=400)

        data = calculate_past_chart(
            time_range=time_range, split_interval=split_interval, service_id=service_id
        )

        return Response(data)

    @action(detail=False, methods=["get"])
    def trackers(self, request):
        data = calculate_trackers_by_status()
        return Response(data)
