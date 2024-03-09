from datetime import timedelta

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

    :return: uptime_percentage and avg_response_time
    """

    uptime_percentage, avg_response_time = None, None
    if not time_range or time_range.value not in QUERY_TIME_RANGE_TYPE.keys():
        return uptime_percentage and avg_response_time
    time_delta = time_range.value
    results = UptimeRecord.objects.filter(
        created_at__gte=now() - timedelta(hours=time_delta)
    )
    # results = UptimeRecord.objects.filter(created_at? range)
    sum_avg_time, sum_uptime = 0, 0
    total_records = results.count()
    for record in results:
        sum_avg_time += record.response_time
        sum_uptime += 1 if record.status else 0
    if total_records:
        avg_response_time = sum_avg_time / total_records
        uptime_percentage = (sum_uptime / total_records) * 100
    return uptime_percentage, avg_response_time
