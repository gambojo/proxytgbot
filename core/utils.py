import random
import string
import re
from datetime import datetime

def generate_code(length: int = 8) -> str:
    """Генерирует случайный код из букв и цифр."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def format_user(user) -> str:
    """Форматирует имя пользователя для отображения."""
    return f"{user.first_name} @{user.username or '—'}"

def format_datetime(dt: datetime) -> str:
    """Форматирует дату в читаемый вид."""
    return dt.strftime("%d.%m.%Y %H:%M")

def is_valid_username(username: str) -> bool:
    """Проверяет валидность Telegram username."""
    return bool(re.fullmatch(r"[a-zA-Z0-9_]{5,32}", username))

def is_valid_email(email: str) -> bool:
    """Простая проверка email."""
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))
