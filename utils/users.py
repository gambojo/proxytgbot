from aiogram import types

def get_user_info(user: types.User) -> dict:
    return {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "language_code": user.language_code,
        "is_bot": user.is_bot
    }
