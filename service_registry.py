import hug
import threading
import requests
import time

services = []  # Holds address of each service


@hug.post("/register/", status=hug.falcon.HTTP_201)
def register(
    url: hug.types.text,
    response,
):
    """POST a new service to the registry"""

    # Add the service to the registry
    try:
        services.append(url)
        print("Registry input:", url)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
    return url


def check_service():
    """Periodically performs a health check on each service in the registry"""
    while True:
        global services
        for url in services:
            r = requests.get(url + "/health-check")
            print('Health check:', url)
            # Remove service if it doesn't pass health check
            if r.status_code != 200:
                services.remove(url)

        time.sleep(60)


# @hug.startup()
def health_check():
    """Creates a daemon thread for performing health checks"""
    x = threading.Thread(target=check_service, args=(), daemon=True)
    x.start()


health_check()
