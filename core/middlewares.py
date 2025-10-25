from typing import Callable, Dict, Any
from aiogram.types import Message, TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from databases.crud import ensure_user_exists
import logging

def logging_middleware() -> BaseMiddleware:
    async def handler(event: Message, data: Dict[str, Any], call_next: Callable):
        logging.info(f"[{event.from_user.id}] {event.text}")
        return await call_next(event, data)

    return BaseMiddleware(handler)

def user_init_middleware():
    class _UserInitMiddleware(BaseMiddleware):
        async def __call__(self, handler, event: TelegramObject, data: dict):
            if isinstance(event, Message):
                user, _ = await ensure_user_exists(
                    telegram_id=event.from_user.id,
                    username=event.from_user.username,
                    first_name=event.from_user.first_name,
                    last_name=event.from_user.last_name
                )
                data["user"] = user
            return await handler(event, data)
    return _UserInitMiddleware()
