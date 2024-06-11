from sqlalchemy import select

from src.core.types.repositories import BaseRepository
from src.db.models import AuthUser


class AuthUserRepository(BaseRepository[AuthUser]):
    model = AuthUser

    async def get_by_username(self, username: str) -> AuthUser:
        query = select(self._model).where(self._model.username == username)
        result = await self._session.execute(query)
        return result.scalar_one()
