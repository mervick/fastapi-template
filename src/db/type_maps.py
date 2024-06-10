import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, UUID, func
from sqlalchemy.orm import mapped_column

datetime_auto_now_add = Annotated[
    datetime,
    mapped_column(TIMESTAMP(timezone=True), server_default=func.now()),
]
datetime_auto_now = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
]
uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(UUID, primary_key=True, default=uuid.uuid4),
]
