import uuid
import base64
import secrets
from py3xui import Client
from proxy_clients.base import api_connect, get_inbound, calculate_expiry_time, get_days_until_expiry
from config import XUI_EXTERNAL_IP, XUI_EXPIRY_TIME, SHADOWSOCKS_INBOUND_ID


async def create_ss_client(email: str, inbound_id: int = SHADOWSOCKS_INBOUND_ID, update_expiry: bool = False,
                           disable_client: bool = False, enable_client: bool = False, days: int = XUI_EXPIRY_TIME,
                           inbound_listner: str = XUI_EXTERNAL_IP, cipher: str = "aes-128-gcm"):
    api = await api_connect()
    inbound = await get_inbound(api, inbound_id)
    expiry_time = calculate_expiry_time(days)
    remark = inbound.remark

    try:
        existing_client = await api.client.get_by_email(email)
        client_is_exists = True
    except Exception:
        existing_client = None
        client_is_exists = False

    # Если клиент существует - получаем его текущие данные
    if existing_client:
        for c in inbound.settings.clients:
            if c.email == email:
                client_id = c.id
                until_expiry = c.expiry_time
                client_is_active = c.enable
                password = c.password
                break
        else:
            client_id = existing_client.id
            until_expiry = existing_client.expiry_time
            client_is_active = existing_client.enable
            password = existing_client.password

        # ОБНОВЛЯЕМ клиента если нужно
        if update_expiry:
            existing_client.expiry_time = expiry_time
            await api.client.update(existing_client.id, existing_client)
            until_expiry = expiry_time

        if enable_client:
            existing_client.enable = True
            await api.client.update(existing_client.id, existing_client)
            client_is_active = True

        if disable_client:
            existing_client.enable = False
            await api.client.update(existing_client.id, existing_client)
            client_is_active = False

    else:
        # СОЗДАЕМ нового клиента
        client_id = str(uuid.uuid4())
        until_expiry = expiry_time
        client_is_active = True
        password = secrets.token_urlsafe(32)
        new_client = Client(
            id=client_id,
            password=password,
            email=email,
            enable=True,
            expiry_time=expiry_time,
            sub_id=str(uuid.uuid4())[:16]
        )
        await api.client.add(inbound_id, [new_client])

    user_info = f"{cipher}:{password}"
    encoded = base64.urlsafe_b64encode(user_info.encode()).decode().rstrip("=")
    connection_string = f"ss://{encoded}@{inbound_listner}:{inbound.port}/?type=tcp#{remark}-{email}"
    expiry_days = get_days_until_expiry(until_expiry)

    return {
        "client_is_exists": client_is_exists,
        "client_id": client_id,
        "expiry_time": expiry_days,
        "client_is_active": client_is_active,
        "connection_string": connection_string
    }


async def get_ss_clients(inbound_id: int = SHADOWSOCKS_INBOUND_ID):
    """Получить всех клиентов Shadowsocks inbound'а"""
    api = await api_connect()
    inbound = await get_inbound(api, inbound_id)
    clients = inbound.settings.clients
    return clients


async def update_client_expiry(email: str, days: int):
    """Обновить срок действия клиента"""
    result = await create_ss_client(email=email, update_expiry=True, days=days)
    return result


async def disable_client(email: str):
    """Отключить клиента"""
    result = await create_ss_client(email=email, disable_client=True)
    return result


async def enable_client(email: str):
    """Включить клиента"""
    result = await create_ss_client(email=email, enable_client=True)
    return result

# import asyncio
# if __name__ == "__main__":
#     ss_client = asyncio.run(create_ss_client(email="785818468"))
#     print(ss_client)