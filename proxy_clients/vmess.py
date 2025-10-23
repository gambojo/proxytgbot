import uuid
import json
import base64
from py3xui import Client
from proxy_clients.base import api_connect, get_inbound, calculate_expiry_time, get_days_until_expiry
from config import XUI_EXTERNAL_IP, XUI_EXPIRY_TIME, VMESS_INBOUND_ID


async def create_vmess_client(email: str, inbound_id: int = VMESS_INBOUND_ID, update_expiry: bool = False,
                              disable_client: bool = False, enable_client: bool = False, days: int = XUI_EXPIRY_TIME,
                              inbound_listner: str = XUI_EXTERNAL_IP):
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
                break
        else:
            client_id = existing_client.id
            until_expiry = existing_client.expiry_time
            client_is_active = existing_client.enable

        # ОБНОВЛЯЕМ клиента если нужно
        if update_expiry:
            existing_client.expiry_time = expiry_time
            await api.client.update(existing_client.id, existing_client)
            until_expiry = expiry_time  # ОБНОВЛЯЕМ локальную переменную

        if enable_client:
            existing_client.enable = True
            await api.client.update(existing_client.id, existing_client)
            client_is_active = True  # ОБНОВЛЯЕМ локальную переменную

        if disable_client:
            existing_client.enable = False
            await api.client.update(existing_client.id, existing_client)
            client_is_active = False  # ОБНОВЛЯЕМ локальную переменную

    else:
        # СОЗДАЕМ нового клиента
        client_id = str(uuid.uuid4())
        until_expiry = expiry_time
        client_is_active = True
        new_client = Client(
            id=client_id,
            email=email,
            enable=True,
            expiry_time=expiry_time,
            sub_id=str(uuid.uuid4())[:16]
        )
        await api.client.add(inbound_id, [new_client])

    # Генерируем connection string
    vmess_config = {
        "v": "2",
        "ps": f"{remark}-{email}",
        "add": inbound_listner,
        "port": int(inbound.port),
        "id": client_id,
        "scy": "auto",
        "net": "tcp",
        "tls": "none",
        "type": "http",
        "path": "/"
    }

    encoded = base64.b64encode(json.dumps(vmess_config, indent=2).encode()).decode()
    connection_string = f"vmess://{encoded}"
    expiry_days = get_days_until_expiry(until_expiry)

    return {
        "client_is_exists": client_is_exists,
        "client_id": client_id,
        "expiry_time": expiry_days,
        "client_is_active": client_is_active,
        "connection_string": connection_string
    }


async def get_vmess_clients(inbound_id: int = VMESS_INBOUND_ID):
    """Получить всех клиентов VMess inbound'а"""
    api = await api_connect()
    inbound = await get_inbound(api, inbound_id)
    clients = inbound.settings.clients
    return clients


async def update_client_expiry(email: str, days: int):
    """Обновить срок действия клиента"""
    result = await create_vmess_client(email=email, update_expiry=True, days=days)
    return result


async def disable_client(email: str):
    """Отключить клиента"""
    result = await create_vmess_client(email=email, disable_client=True)
    return result


async def enable_client(email: str):
    """Включить клиента"""
    result = await create_vmess_client(email=email, enable_client=True)
    return result

# import asyncio
# if __name__ == "__main__":
#     vmess_client = asyncio.run(create_vmess_client(email="785818469"))
#     print(vmess_client)