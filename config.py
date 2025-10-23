import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_IDS = [785818468]
BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

XUI_PANEL_URL = os.getenv("XUI_PANEL_URL")
XUI_USERNAME = os.getenv("XUI_USERNAME")
XUI_PASSWORD = os.getenv("XUI_PASSWORD")

XUI_EXTERNAL_IP = os.getenv("XUI_EXTERNAL_IP")
XUI_EXPIRY_TIME = int(os.getenv("XUI_EXPIRY_TIME"))
VLESS_INBOUND_ID = int(os.getenv("VLESS_INBOUND_ID"))
VMESS_INBOUND_ID = int(os.getenv("VMESS_INBOUND_ID"))
SHADOWSOCKS_INBOUND_ID = int(os.getenv("SHADOWSOCKS_INBOUND_ID"))
TROJAN_INBOUND_ID = int(os.getenv("TROJAN_INBOUND_ID"))

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
