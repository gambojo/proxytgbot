from .db import engine, Base
from core.config import settings
from alembic.config import Config
from alembic import command

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
