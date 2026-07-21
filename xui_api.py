import os
import requests
import uuid
import time


PANEL_URL = os.getenv("PANEL_URL")
PANEL_USERNAME = os.getenv("PANEL_USERNAME")
PANEL_PASSWORD = os.getenv("PANEL_PASSWORD")


session = requests.Session()


def login_panel():
    url = f"{PANEL_URL}/login"

    data = {
        "username": PANEL_USERNAME,
        "password": PANEL_PASSWORD
    }

    r = session.post(url, data=data)

    return r.status_code == 200



def create_vless_user():

    if not login_panel():
        return None


    client_uuid = str(uuid.uuid4())

    email = f"user{int(time.time())}"


    return {
        "uuid": client_uuid,
        "email": email
    }
