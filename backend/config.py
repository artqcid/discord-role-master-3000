"""Application settings loaded from .env via pydantic-settings."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configurable application settings."""

    discord_bot_token: str
    guild_id: str
    database_url: str = "sqlite+aiosqlite:///./discord_rm.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings singleton."""
    return Settings()
