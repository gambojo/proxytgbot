from aiogram.filters import Filter
from aiogram.types import Message
from databases.crud import get_user_by_telegram_id

def role_filter(required_role: str) -> Filter:
    async def check(msg: Message) -> bool:
        user = await get_user_by_telegram_id(msg.from_user.id)
        return getattr(user, "role", None) == required_role
    return Filter(func=check)
