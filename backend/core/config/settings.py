import logging
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_logger = logging.getLogger(__name__)


def _resolve_env_file() -> str | None:
    app_env = os.getenv("APP_ENV", "dev")
    for candidate in [Path(f".env.{app_env}"), Path(".env")]:
        if candidate.is_file():
            return str(candidate)
    return None


_ENV_FILE = _resolve_env_file()


class LicenseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

    license_key: str = Field(..., alias="LICENSE_KEY")
    license_server_url: str = Field("https://license.wyunsi.com", alias="LICENSE_SERVER_URL")
    deployment_id: str = Field(..., alias="DEPLOYMENT_ID")


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=_ENV_FILE, extra="ignore")

    url: str = Field(..., description="DB_URL")
    pool_size: int = Field(10)
    max_overflow: int = Field(10)
    pool_pre_ping: bool = Field(True)
    pool_recycle: int = Field(3600)
    pool_timeout: int = Field(30)
    echo: bool = Field(False)


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=_ENV_FILE, extra="ignore")

    url: str = Field("redis://localhost:6379/0", description="REDIS_URL")
    key_prefix: str = Field("api")
    max_connections: int = Field(50)
    socket_timeout: int = Field(5)
    socket_connect_timeout: int = Field(3)


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELERY_", env_file=_ENV_FILE, extra="ignore")

    broker_url: str = Field(..., description="CELERY_BROKER_URL")
    result_backend: str | None = Field(None)
    task_serializer: str = Field("json")
    result_serializer: str = Field("json")
    timezone: str = Field("UTC")
    outbox_poll_interval: int = Field(5, ge=1, le=60)


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=_ENV_FILE, extra="ignore")

    level: str = Field("INFO")
    file_enabled: bool = Field(False)
    file_path: str = Field("logs/app.log")
    slow_request_threshold: int = Field(3000)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE, extra="ignore")

    app_name: str = Field("api")
    app_env: str = Field("dev")
    debug: bool = Field(False)
    enable_docs: bool = Field(True)
    app_secret_key: str = Field(..., alias="APP_SECRET_KEY")

    license: LicenseSettings = LicenseSettings()  # type: ignore[call-arg]
    db: DatabaseSettings = DatabaseSettings()  # type: ignore[call-arg]
    redis: RedisSettings = RedisSettings()  # type: ignore[call-arg]
    celery: CelerySettings = CelerySettings()  # type: ignore[call-arg]
    log: LogSettings = LogSettings()  # type: ignore[call-arg]


settings = Settings()  # type: ignore[call-arg]
