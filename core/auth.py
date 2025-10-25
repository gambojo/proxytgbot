from core.config import settings

def determine_role(telegram_id: int) -> str:
    if telegram_id in settings.admin_ids:
        return "admin"
    return "user"

def is_admin(user) -> bool:
    return getattr(user, "is_admin", False) or getattr(user, "role", None) == "admin"

def has_role(user, role: str) -> bool:
    return getattr(user, "role", None) == role

def has_any_role(user, roles: list[str]) -> bool:
    return getattr(user, "role", None) in roles

def require_role(user, role: str):
    if not has_role(user, role):
        raise PermissionError(f"⛔ Требуется роль: {role}")

def require_any_role(user, roles: list[str]):
    if not has_any_role(user, roles):
        raise PermissionError(f"⛔ Требуется одна из ролей: {', '.join(roles)}")
