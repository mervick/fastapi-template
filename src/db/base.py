import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, UUID, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.db.type_maps import datetime_auto_now, datetime_auto_now_add, uuid_pk

POSTGRES_NAMING_CONVENTION = {
    "ix": "%(table_name)s_%(column_0_N_name)s_idx",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class SAModel(DeclarativeBase):
    __tablename__: str
    metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
        uuid.UUID: Annotated[
            uuid.UUID,
            mapped_column(UUID, default=uuid.uuid4),
        ],
    }

    id: Mapped[uuid_pk]
    created_at: Mapped[datetime_auto_now_add]
    updated_at: Mapped[datetime_auto_now]
