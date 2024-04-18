from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone
from django.utils.timezone import now

from apps.monitoring.models import UptimeRecord
from apps.service.models import Service

QUERY_TIME_RANGE_TYPE = {
    1: "Last 1 hour",
    3: "Last 3 hours",
    6: "Last 6 hours",
    24: "Last 24 hours",
    168: "Last 7 days",
    720: "Last 30 days",
    -1: "All time",
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


def calculate_past_chart(time_range, split_interval, service_id=None):
    """
    Given a time range in HOUR, query all UptimeRecord and
    calculate uptime_percentage and the average_response_time in the interval for chart,
    the interval is calculated by showing 30 records in the chart. E.g. if the time_range is 720 hours,
    the chart will show 30 records, each record represents 24 hours.
    :return: a json contains a summary of uptime percentage and average response time, following 30 detailed records
    where each record contains total_records, uptime_percentage, average_response_time, time_start and time_end

    """
    if not service_id or not Service.objects.filter(id=service_id).exists():
        return KeyError("Invalid service id")
    service_name = Service.objects.get(id=service_id).name
    monitoring_method = Service.objects.get(id=service_id).monitoring_type

    if (not time_range) or (time_range not in QUERY_TIME_RANGE_TYPE.keys()):
        return KeyError("Invalid time range")
    # iterate 30 intervals in the given time range
    if split_interval < 1:
        split_interval = 1
    delta = timedelta(hours=time_range / split_interval)
    start_time = now() - timedelta(hours=time_range)
    total_records, total_up_records = 0, 0
    all_results = []
    total_avg_response_time = []

    for _ in range(split_interval):
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
                "uptime_percentage": (interval_up_records / interval_total_records)
                * 100
                if interval_total_records
                else 0,
                "average_response_time": average_response_time,
                "time_start": timezone.localtime(end_time).strftime("%b. %-d, %H:%M"),
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

    # format the uptime_percentage and total_avg_response_time
    uptime_percentage = round(uptime_percentage, 2)
    total_avg_response_time = round(total_avg_response_time, 0)
    summary = {
        "service_name": service_name,
        "monitoring_method": monitoring_method.upper(),
        "errors": total_records - total_up_records,
        "total_records": total_records,
        "uptime_percentage": uptime_percentage,
        "average_response_time": total_avg_response_time,
        "time_start": timezone.localtime(now()).strftime("%b. %-d, %H:%M"),
        "time_end": timezone.localtime(now()).strftime("%b. %-d, %H:%M"),
    }
    response = {
        "summary": summary,
        "data": all_results,
    }
    return response


def calculate_trackers_by_status():
    """
    Query all UptimeRecords and calculate last 30days of tracker status and overall 30days uptime percentage
    tracker status: if its `Operational`: no downtime in the day; or `Down`: has downtime in the day;
    `Degraded`: has downtime but not all day
    :return: a json contains all the service status in the last 30 days;
    e.g. { service_name1: { uptime: 99.9%, status: { Operational, Operational, Down, Operational ,... Degraded } } }

    """

    # get the last 30 days
    start_time = now() - timedelta(days=30)
    results = UptimeRecord.objects.filter(created_at__gte=start_time)
    all_results = {}
    for day in range(30):
        day_results = results.filter(
            created_at__gte=start_time + timedelta(days=day),
            created_at__lt=start_time + timedelta(days=day + 1),
        )
        for record in day_results:
            service_name = record.service.name
            if service_name not in all_results:
                all_results[service_name] = {
                    "total_records_by_day": [0] * 30,
                    "up_records_by_day": [0] * 30,
                }
            if record.status:
                all_results[service_name]["up_records_by_day"][day] += 1
            all_results[service_name]["total_records_by_day"][day] += 1

    for service_name in all_results:
        total_records = sum(all_results[service_name]["total_records_by_day"])
        up_records = sum(all_results[service_name]["up_records_by_day"])
        uptime_percentage = (up_records / total_records) * 100 if total_records else 0
        status = []
        for up, total in zip(
            all_results[service_name]["up_records_by_day"],
            all_results[service_name]["total_records_by_day"],
        ):
            if up == 0:
                status.append("Down")
            elif up == total:
                status.append("Operational")
            else:
                status.append("Degraded")
        all_results[service_name].pop("total_records_by_day")
        all_results[service_name].pop("up_records_by_day")
        all_results[service_name]["uptime_percentage"] = uptime_percentage
        all_results[service_name]["status"] = status
    return all_results
