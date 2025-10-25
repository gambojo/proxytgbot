from .db import engine, Base
from core.config import settings
from alembic.config import Config
from alembic import command

async def init():
    async with engine.begin() as conn:
        if settings.db_is_sqlite:
            await conn.run_sync(Base.metadata.create_all)
        elif settings.db_is_postgres:
            cfg = Config("")
            cfg.set_main_option("script_location", "databases")
            cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
            command.upgrade(cfg, "head")
        else:
            print(f"⚠️ Unknown DB type: {settings.db_scheme}")
