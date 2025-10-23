from py3xui import AsyncApi
from datetime import datetime, timedelta
from config import XUI_PANEL_URL, XUI_USERNAME, XUI_PASSWORD

async def api_connect():
    api = AsyncApi(XUI_PANEL_URL, XUI_USERNAME, XUI_PASSWORD)
    await api.login()
    return api

async def get_inbound(api, inbound_id):
    return await api.inbound.get_by_id(inbound_id)

def calculate_expiry_time(days: int) -> int:
    if days <= 0:
        return 0
    expire_dt = datetime.now() + timedelta(days=days)
    return int(expire_dt.timestamp() * 1000)

def get_days_until_expiry(expiry_time_ms: int) -> int:
    if expiry_time_ms == 0:
        return 0
    now_ms = int(datetime.now().timestamp() * 1000)
    delta_ms = expiry_time_ms - now_ms
    days = delta_ms // (1000 * 60 * 60 * 24)
    return max(days + 1, 0)
