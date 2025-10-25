from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cached_property

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: str

    DATABASE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    XUI_PANEL_URL: str
    XUI_USERNAME: str
    XUI_PASSWORD: str

    XUI_EXTERNAL_IP: str
    XUI_EXPIRY_TIME: int
    VLESS_INBOUND_ID: int
    VMESS_INBOUND_ID: int
    SHADOWSOCKS_INBOUND_ID: int
    TROJAN_INBOUND_ID: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def admin_ids(self) -> list[int]:
        return [int(x) for x in self.ADMIN_IDS.strip("[]").split(",") if x]

    @cached_property
    def db_scheme(self) -> str:
        # Пример: "sqlite", "postgresql", "mysql", "oracle"
        return self.DATABASE_URL.split("://")[0].lower()

    @property
    def db_is_sqlite(self) -> bool:
        return self.db_scheme == "sqlite"

    @property
    def db_is_postgres(self) -> bool:
        return self.db_scheme.startswith("postgres")

settings = Settings()
