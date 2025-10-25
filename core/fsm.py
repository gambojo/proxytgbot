from enum import Enum

# 🔐 Подтверждение действий
class ConfirmState(Enum):
    WAITING = "confirm:waiting"
    CONFIRMED = "confirm:confirmed"
    CANCELLED = "confirm:cancelled"

# 👤 Сценарии пользователя
class UserState(Enum):
    AWAITING_EMAIL = "user:awaiting_email"
    AWAITING_PHONE = "user:awaiting_phone"
    AWAITING_NAME = "user:awaiting_name"

# 🛡 Админские сценарии
class AdminState(Enum):
    AWAITING_BROADCAST_TEXT = "admin:awaiting_broadcast_text"
    AWAITING_ROLE_ASSIGNMENT = "admin:awaiting_role_assignment"
