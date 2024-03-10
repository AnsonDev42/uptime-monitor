from datetime import timedelta

from django.db.models import Avg
from django.utils.timezone import now

from apps.monitoring.models import UptimeRecord


QUERY_TIME_RANGE_TYPE = {
    1: "Last 1 hour",
    3: "Last 3 hours",
    6: "Last 6 hours",
    24: "Last 24 hours",
    168: "Last 7 days",
    720: "Last 30 days",
}


def calculate_past(time_range=None):
    """
    Given an time range in HOUR?DATE, query all UptimeRecord and
    calculate uptime percentage and the average response time

    :return:total_records, uptime_percentage and avg_response_time
    """
    uptime_percentage, avg_response_time = None, None
    if (not time_range) or (time_range not in QUERY_TIME_RANGE_TYPE.keys()):
        return uptime_percentage and avg_response_time
    time_delta = time_range
    results = UptimeRecord.objects.filter(
        created_at__gte=now() - timedelta(hours=time_delta)
    )
    total_records = results.count()
    up_records = results.filter(status=True).count()
    average_response_time = (
        results.filter(status=True).aggregate(Avg("response_time"))[
            "response_time__avg"
        ]
        or 0
    )

    uptime_percentage = (up_records / total_records) * 100 if total_records else 0

    return total_records, uptime_percentage, average_response_time
