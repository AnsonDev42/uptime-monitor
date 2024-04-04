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


def calculate_past_summary(time_range=None):
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


def calculate_past_chart(time_range=None):
    """
    Given a time range in HOUR, query all UptimeRecord and
    calculate uptime_percentage and the average_response_time in the interval for chart,
    the interval is calculated by showing 30 records in the chart. E.g. if the time_range is 720 hours,
    the chart will show 30 records, each record represents 24 hours.
    :return: a json contains a summary of uptime percentage and average response time, following 30 detailed records
    where each record contains total_records, uptime_percentage, average_response_time, time_start and time_end

    """
    if (not time_range) or (time_range not in QUERY_TIME_RANGE_TYPE.keys()):
        return KeyError("Invalid time range")
    # iterate 30 intervals in the given time range
    delta = timedelta(hours=time_range / 30)
    start_time = now() - timedelta(hours=time_range)
    total_records, total_up_records = 0, 0
    all_results = []
    total_avg_response_time = []
    for _ in range(30):
        end_time = start_time + delta
        results = UptimeRecord.objects.filter(
            created_at__gte=start_time, created_at__lt=end_time
        )
        interval_total_records = results.count()
        interval_up_records = results.filter(status=True).count()
        average_response_time = (
            results.filter(status=True).aggregate(Avg("response_time"))[
                "response_time__avg"
            ]
            or 0
        )
        all_results.append(
            {
                "total_records": interval_total_records,
                "uptime_percentage": (interval_up_records / interval_total_records)
                * 100
                if interval_total_records
                else 0,
                "average_response_time": average_response_time,
                "time_start": start_time,
                "time_end": end_time,
            }
        )
        total_records += interval_total_records
        total_up_records += interval_up_records
        total_avg_response_time.append(average_response_time)
        start_time = end_time

    total_avg_response_time = sum(total_avg_response_time) / len(
        total_avg_response_time
    )
    uptime_percentage = (total_up_records / total_records) * 100 if total_records else 0
    all_results.insert(
        0,
        {
            "total_records": total_records,
            "uptime_percentage": uptime_percentage,
            "average_response_time": total_avg_response_time,
            "time_start": now() - timedelta(hours=time_range),
            "time_end": now(),
        },
    )
    return all_results
