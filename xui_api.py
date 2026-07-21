import os
import requests
import uuid
import time

PANEL_URL = os.getenv("PANEL_URL")
PANEL_API_TOKEN = os.getenv("PANEL_API_TOKEN")

session = requests.Session()

session.headers.update({
    "Authorization": f"Bearer {PANEL_API_TOKEN}",
    "Content-Type": "application/json"
})


def create_vless_user():
    client_uuid = str(uuid.uuid4())
    email = f"user{int(time.time())}"

    payload = {
        "up": 0,
        "down": 0,
        "total": 107374182400,
        "remark": email,
        "enable": True,
        "expiryTime": 0,
        "listen": "",
        "port": 0,
        "protocol": "vless",
        "settings": {
            "clients": [
                {
                    "id": client_uuid,
                    "email": email,
                    "flow": ""
                }
            ],
            "decryption": "none",
            "fallbacks": []
        },
        "streamSettings": {},
        "sniffing": {}
    }

    try:
        r = session.post(
            f"{PANEL_URL}/panel/api/inbounds/add",
            json=payload,
            timeout=20
        )

        print("STATUS:", r.status_code)
        print("TEXT:", r.text)

        if r.status_code == 200:
            return {
                "uuid": client_uuid,
                "email": email
            }

        return None

    except Exception as e:
        print(e)
        return None
