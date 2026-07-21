# xui_api.py

import requests
import uuid
import time
import random


class XUI:

    def __init__(
        self,
        panel_url,
        username,
        password
    ):

        self.panel_url = panel_url.rstrip("/")
        self.username = username
        self.password = password

        self.session = requests.Session()

        self.inbounds = [
            1,
            2,
            3
        ]


    # ----------------------
    # LOGIN
    # ----------------------

    def login(self):

        url = f"{self.panel_url}/login"

        data = {
            "username": self.username,
            "password": self.password
        }

        r = self.session.post(
            url,
            json=data,
            timeout=15
        )


        if r.status_code != 200:
            raise Exception(
                "3x-ui login failed"
            )


        result = r.json()


        if not result.get("success", False):
            raise Exception(result)


        return True



    # ----------------------
    # UUID
    # ----------------------

    def generate_uuid(self):

        return str(uuid.uuid4())



    # ----------------------
    # EXPIRATION
    # ----------------------

    def expire_time(self, days):

        return int(
            (time.time() + days * 86400) * 1000
        )



    # ----------------------
    # SELECT INBOUND
    # ----------------------

    def select_inbound(self):

        return random.choice(
            self.inbounds
        )



    # ----------------------
    # CREATE CLIENT
    # ----------------------

    def create_client(
        self,
        email,
        volume_gb,
        days
    ):

        inbound_id = self.select_inbound()

        client_uuid = self.generate_uuid()


        total_bytes = (
            volume_gb
            *
            1024
            *
            1024
            *
            1024
        )


        expire = self.expire_time(days)


        sub_id = uuid.uuid4().hex[:16]


        client = {

            "id": client_uuid,
            "email": email,
            "flow": "",
            "limitIp": 0,
            "totalGB": total_bytes,
            "expiryTime": expire,
            "enable": True,
            "tgId": "",
            "subId": sub_id

        }


        payload = {

            "id": inbound_id,

            "settings":
                '{"clients":['
                +
                str(client).replace("'", '"')
                +
                ']}'

        }


        url = (
            f"{self.panel_url}"
            f"/panel/api/inbounds/addClient"
        )


        r = self.session.post(
            url,
            data=payload,
            timeout=15
        )


        result = r.json()


        if not result.get("success", False):

            raise Exception(result)


        return {

            "uuid": client_uuid,
            "email": email,
            "inbound": inbound_id,
            "volume": volume_gb,
            "days": days,
            "expire": expire,
            "subscription":
                self.subscription_link(sub_id)

        }
