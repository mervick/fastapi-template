from asyncpg.exceptions import TooManyConnectionsError
from fastapi import FastAPI
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.asyncpg import AsyncPGIntegration
from sentry_sdk.integrations.loguru import LoguruIntegration
from sqlalchemy.exc import IntegrityError
from starlette.middleware.cors import CORSMiddleware

from src.config.routers import api_v1_router, services_router
from src.config.settings import settings
from src.core.api.exceptions.handlers import (
    database_too_many_connections_error_handler,
    unique_violation_error_handler,
)
from src.core.types.singleton import SingletonMeta


class ApplicationConfig(metaclass=SingletonMeta):
    __slots__ = ("_asgi_app",)
    _asgi_app: FastAPI

    def __init__(self) -> None:
        """
        Setting up ASGI get_app.
        """

        if settings.SENTRY_DSN:
            sentry_init(
                dsn=settings.SENTRY_DSN,
                enable_tracing=True,
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
                integrations=[
                    AsyncioIntegration(),
                    AsyncPGIntegration(),
                    LoguruIntegration(),
                ],
            )

        self._asgi_app = FastAPI(
            title=settings.PROJECT_NAME,
            version="1.0",
            description="API Documentation for FastAPI Template",
            docs_url=f"{settings.API_V1_STR}/docs",
            redoc_url=f"{settings.API_V1_STR}/redoc",
            openapi_url=f"{settings.API_V1_STR}/openapi.json",
        )
        self._collect_middleware()
        self._collect_exception_handler()
        self._asgi_app.include_router(api_v1_router)
        self._asgi_app.include_router(services_router)

    def _collect_middleware(self) -> None:
        """
        Collecting all middleware for ASGI get_app here
        """

        if settings.BACKEND_CORS_ORIGINS:
            self._asgi_app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

    def _collect_exception_handler(self) -> None:
        self._asgi_app.exception_handler(IntegrityError)(
            unique_violation_error_handler,
        )
        self._asgi_app.exception_handler(TooManyConnectionsError)(
            database_too_many_connections_error_handler,
        )

    def get_app(self) -> FastAPI:
        """Get ASGI get_app."""

        return self._asgi_app
