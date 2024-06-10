from enum import StrEnum
from typing import Any

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.dialects.postgresql import ENUM


class SAStrEnum(TypeDecorator[ENUM]):
    """
    Usage:

    ```python
    # model
    class MyModel(SAModel):
        enum_field: Mapped[EnumBasedClass] = mapped_column(
            SAStrEnum(EnumBasedClass),
        )

    # alembic
    # on upgrade:
    sa.Column(
        "enum_field",
        SAStrEnum(EnumBasedClass),
        nullable=False,
    ),

    # on downgrade:
    sa.Enum(name="enumbasedclass").drop(op.get_bind(), checkfirst=False)
    ```
    """

    impl = ENUM
    cache_ok = True

    _enumtype: type[StrEnum]

    def __init__(self, enumtype: type[StrEnum], **kwargs: Any) -> None:
        values = [str(v) for v in enumtype]
        kwargs["name"] = kwargs.pop("name", enumtype.__name__.lower())
        kwargs["native_enum"] = kwargs.pop("native_enum", True)
        kwargs["validate_strings"] = kwargs.pop("validate_strings", True)
        super().__init__(*values, **kwargs)
        self._enumtype = enumtype

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        _ = dialect
        return self._enumtype(value) if value is not None else None
