import sys
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic import PostgresDsn, field_validator
from pydantic._internal._model_construction import ModelMetaclass
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.types.singleton import SingletonMeta


class MySettingsMeta(SingletonMeta, ModelMetaclass):
    ...


class Settings(BaseSettings, metaclass=MySettingsMeta):
    """
    Base settings for all backend.
    """

    ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()

    # Base
    DEBUG: bool = False
    SECRET_KEY: str = "super-secret-key"

    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    API_V1_STR: str = "/api/v1"

    PROJECT_NAME: str = "FastAPI Template"

    SENTRY_DSN: str = ""

    # Postgres
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USERNAME: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    POSTGRES_URL: str = ""

    @field_validator("POSTGRES_URL", mode="before")
    @classmethod
    def assemble_postgres_url(cls, v: Any, info: ValidationInfo) -> str:
        if isinstance(v, str) and v:
            return v

        postgres_dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["POSTGRES_USERNAME"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_HOST"],
            port=info.data["POSTGRES_PORT"],
            path=info.data["POSTGRES_DB"],
        )
        return str(postgres_dsn)

    model_config = SettingsConfigDict(
        env_file=f"{ROOT_DIR}/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True,
        extra="ignore",  # ignores extra keys from env file
        frozen=True,
    )


settings = Settings()

# Logging Configuration
logger.remove(0)
logger.add(
    sys.stderr,
    format="<red>[{level}]</red> Message : <green>{message}</green> @ {time:YYYY-MM-DD HH:mm:ss}",
    colorize=True,
    level=("DEBUG" if settings.DEBUG else "INFO"),
    backtrace=True,
    diagnose=True,
)
