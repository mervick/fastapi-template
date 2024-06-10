from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import SAModel


class AuthUser(SAModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str | None] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    hashed_password: Mapped[str]
