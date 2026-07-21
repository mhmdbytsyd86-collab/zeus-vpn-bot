import os
import requests


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

    response = session.post(url, data=data)

    if response.status_code == 200:
        return True

    return False


def get_panel_status():
    if login_panel():
        return "✅ اتصال به پنل موفق بود"
    else:
        return "❌ اتصال به پنل ناموفق بود"
