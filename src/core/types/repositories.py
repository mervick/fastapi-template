from collections.abc import Sequence
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import SAModel

_MT = TypeVar("_MT", bound=SAModel)


class BaseRepository(Generic[_MT]):
    _model: type[_MT]
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id_: UUID) -> _MT:
        """
        Get model instance by id
        """
        query = select(self._model).where(self._model.id == id_)
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_all(self) -> Sequence[_MT]:
        """
        Get all model instances
        """
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def save(self, instance: _MT) -> _MT:
        """
        Save a new model instance or update if exists
        """
        inspr = inspect(instance)
        if not inspr.modified and inspr.has_identity:
            return instance

        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)

        return instance

    async def delete(self, instance: _MT) -> None:
        """
        Delete a model instance from database
        """
        await self._session.delete(instance)
        await self._session.flush()
