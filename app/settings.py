"""Application settings."""

from pydantic import AliasChoices, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class for managing environment variables and configuration."""

    model_config = SettingsConfigDict(env_file=".env")

    google_ai_api_key: SecretStr = Field(
        validation_alias=AliasChoices("GOOGLE_AI_API_KEY", "GOOGLE_AI_PAID_API_KEY"),
    )
    bb_url: HttpUrl
    bb_password: SecretStr
    env: str


settings = Settings()  # pyright: ignore [reportCallIssue]
