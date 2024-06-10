from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.application import ApplicationConfig
from src.config.settings import settings
from src.core.dependencies.db import get_async_session


@pytest.fixture(scope="session", autouse=True)
async def _override_fastapi_dependencies(session: AsyncSession) -> None:
    async def _get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield session
        except IntegrityError as exc:
            await session.rollback()
            raise exc

    app = ApplicationConfig().get_app()
    app.dependency_overrides[get_async_session] = _get_test_async_session


@pytest.fixture(scope="session")
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    app = ApplicationConfig().get_app()
    async with AsyncClient(app=app, base_url=f"http://{settings.SERVER_HOST}") as client:
        yield client
