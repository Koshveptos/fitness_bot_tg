import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # exxx
    DATABASE_SQLITE = "sqlite+aiosqlite:///data/db.sqlite3"
    TG_KEY = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )


settings = Settings()
