import hug
import threading
import requests
import time
import os
import socket


def check_service(ports):
    while True:
        for port in ports:
            print("Port:", port)
            r = requests.get("http://localhost:" + str(port) + "/health")
            print("Status code:", r.status_code)
            if r.status_code != 200:
                pass

        time.sleep(60)


@hug.startup()
def health_check():
    # TODO get service ports
    print("Environ get:", os.environ.get("PORT"))
    ports = [8000, 8100]

    x = threading.Thread(target=check_service, args=(ports,), daemon=True)
    x.start()
    time.sleep(60)


# health_check()
