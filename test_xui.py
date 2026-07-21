from xui_api import XUI


xui = XUI(
    "https://3x-ui-production-1903.up.railway.app",
    "mobin",
    "Mm009900**"
)


xui.login()


user = xui.create_client(
    email="telegram_12345",
    volume_gb=100,
    days=30
)


print(user)
