import requests


def check_service_status(url):
    """ "
    Check if a service is up or down and return the response time in ms
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True, response.elapsed.total_seconds() * 1000, None
    except requests.exceptions.RequestException as e:
        return False, 0, e


if __name__ == "__main__":
    print(check_service_status("https://www.google.com"))
