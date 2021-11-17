import hug
import threading
import requests
import time

# Hard coded ports for each service
services = [
    "http://localhost:4000",
    "http://localhost:4100",
    "http://localhost:4200",
    "http://localhost:4300",
]
# services = []


def check_service():
    while True:
        global services
        for url in services:
            r = requests.get(url + "/health-check")
            # Remove service if it doesn't pass health check
            if r.status_code != 200:
                services.remove(url)

        time.sleep(60)


@hug.post("/register/", status=hug.falcon.HTTP_201)
def register(
    url: hug.types.text,
    response,
):
    """POST a new service to the registry"""

    print("Registry input:", url)
    try:
        services.append(url)
        print(services)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error": str(e)}
    return url


# @hug.startup()
def health_check():
    x = threading.Thread(target=check_service, args=(), daemon=True)
    x.start()


health_check()
