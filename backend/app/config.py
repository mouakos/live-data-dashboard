from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration settings."""

    database_url: str = "sqlite+aiosqlite:///data.db"
    database_echo: bool = Field(default=False)
    broadcast_interval_seconds: float = 1.0
    memory_window: int = 500
    ws_route: str = "/ws"
    allowed_origins: str
    database_echo: bool = Field(default=False)
    default_snapshot_size: int = Field(default=120, ge=1, le=120)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Config()
