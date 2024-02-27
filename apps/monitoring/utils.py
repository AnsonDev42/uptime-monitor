import requests


def check_service_status(url):
    """ "
    Check if a service is up or down and return the response time
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True, response.elapsed.total_seconds()
    except requests.exceptions.RequestException:
        return False, 0
