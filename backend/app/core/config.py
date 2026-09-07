"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/real_estate_lead_bot"

    gemini_api_key: str | None = None

    n8n_webhook_url: str | None = None
    n8n_webhook_secret: str | None = None
    n8n_api_key: str | None = None

    google_sheets_id: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
