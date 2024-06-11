from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config.settings import settings


class AsyncSessionMaker:
    _engine = create_async_engine(
        url=settings.POSTGRES_URL,
        pool_pre_ping=True,
        future=True,
    )
    _sessionmaker = async_sessionmaker(
        bind=_engine,
        autoflush=False,
        autocommit=False,
    )

    def __init__(self) -> None:
        self._session = self._sessionmaker()

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def __aenter__(self) -> AsyncSession:
        return await self._session.__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return await self._session.__aexit__(exc_type, exc_value, traceback)
