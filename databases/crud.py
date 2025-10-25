from sqlalchemy import select
from .models import User
from .db import SessionLocal
from core.auth import determine_role


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

async def create_user(telegram_id: int, username: str = None, first_name: str = None,
                      last_name: str = None, role: str = "user") -> User:
    async with SessionLocal() as session:
        is_admin = role == "admin"
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            role=role
        )
        session.add(user)
        await session.commit()
        return user

async def ensure_user_exists(telegram_id: int, username: str = None, first_name: str = None,
                             last_name: str = None, role: str = "user") -> tuple[User, bool]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            return user, False

        role = determine_role(telegram_id)
        is_admin = role == "admin"

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            role=role
        )
        session.add(user)
        await session.commit()
        return user, True

async def update_user(telegram_id: int, **kwargs) -> User | None:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await session.commit()
        return user

async def delete_user(telegram_id: int) -> bool:
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True
