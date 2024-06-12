import contextlib
from collections.abc import AsyncGenerator

import alembic
import alembic.command
import alembic.config
import asyncpg
import pytest
import pytest_asyncio
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine

from src.config.settings import settings
from src.core.tests.utils import upgrade_database


@pytest.fixture(scope="session")
def postgres_test_db_name(request: pytest.FixtureRequest) -> str:
    db_name = f"test-{settings.POSTGRES_DB}"
    xdist_suffix = getattr(request.config, "workerinput", {}).get("workerid")
    if xdist_suffix:
        # Put a suffix like _gw0, _gw1 etc on xdist processes
        db_name += f"_{xdist_suffix}"
    return db_name


@pytest.fixture(scope="session")
def postgres_test_db_url(postgres_test_db_name: str) -> str:
    postgres_dsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        path=postgres_test_db_name,
    )
    return str(postgres_dsn)


@pytest.fixture(scope="session", autouse=True)
async def _create_test_db_if_not_exists(postgres_test_db_name: str) -> None:
    adapted_postgres_url = settings.POSTGRES_URL.replace("postgresql+asyncpg", "postgresql")
    conn = await asyncpg.connect(adapted_postgres_url)
    with contextlib.suppress(asyncpg.DuplicateDatabaseError):
        await conn.execute(f'CREATE DATABASE "{postgres_test_db_name}"')


@pytest.fixture(scope="session", autouse=True)
@pytest.mark.usefixtures(  # noqa: PT025
    # used for application order
    "_create_test_db_if_not_exists",
)
def _mock_postgres_url(postgres_test_db_url: str, monkeysession: pytest.MonkeyPatch) -> None:
    monkeysession.setattr("src.config.settings.settings.POSTGRES_URL", postgres_test_db_url)


@pytest_asyncio.fixture(scope="session")
async def connection(postgres_test_db_url: str) -> AsyncGenerator[AsyncConnection, None]:
    """
    Set up database connection.
    """

    engine = create_async_engine(
        url=postgres_test_db_url,
        pool_pre_ping=True,
    )

    async with engine.connect() as conn:
        yield conn


@pytest_asyncio.fixture(scope="session")
async def alembic_config(postgres_test_db_url: str) -> alembic.config.Config:
    """
    Alembic config generated from context.
    """
    config = alembic.config.Config(
        settings.ROOT_DIR / "alembic.ini",
    )

    config.set_main_option(
        "sqlalchemy.url",
        postgres_test_db_url,
    )
    return config


@pytest_asyncio.fixture(scope="session", autouse=True)
@pytest.mark.usefixtures(
    # used for application order
    "_mock_postgres_url",
)
async def _migrate_database(
    connection: AsyncConnection,
    alembic_config: alembic.config.Config,
) -> None:
    """
    Migrate database to latest revision.
    """

    await connection.run_sync(upgrade_database, alembic_config)


@pytest_asyncio.fixture(autouse=True)
@pytest.mark.usefixtures(
    # used for application order
    "_migrate_database",
)
async def _pg_transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[None, None]:
    """
    Wrap each test in a 100% rollback transaction.
    """

    transaction = connection
    await transaction.begin()

    yield

    await transaction.rollback()


@pytest.fixture(scope="session")
async def session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=connection) as session:
        yield session
