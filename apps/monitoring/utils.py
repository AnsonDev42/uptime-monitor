import requests
from requests.exceptions import RequestException


def check_service_status(url):
    try:
        response = requests.get(url, timeout=5)  # 5 seconds timeout
        return (
            True,
            response.elapsed.total_seconds(),
        )  # Service is up, return response time
    except RequestException:
        return False, None  # Service is down or unreachable
