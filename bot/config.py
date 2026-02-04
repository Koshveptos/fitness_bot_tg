# bot/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Основная строка подключения к БД (можно переопределить в .env)
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/db.sqlite3"

    # Токен Telegram-бота
    TG_TOKEN: str = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # если в .env будут лишние ключи — не ругаться
    )


settings = Settings()
