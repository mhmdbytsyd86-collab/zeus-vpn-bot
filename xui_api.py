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

    try:
        r = session.post(url, data=data, timeout=10)

        print("LOGIN STATUS:", r.status_code)
        print("LOGIN RESPONSE:", r.text)

        return r.status_code == 200

    except Exception as e:
        print("LOGIN ERROR:", e)
        return False



def create_vless_user():

    if not login_panel():
        print("Panel login failed")
        return None


    client_uuid = str(uuid.uuid4())

    email = f"user{int(time.time())}"


    print("NEW USER UUID:", client_uuid)


    return {
        "uuid": client_uuid,
        "email": email
    }
