from pydantic import EmailStr, field_validator
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo

from src.core.dto import BaseDTO


class AuthUserCreateDTO(BaseDTO):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    password: str
    repeated_password: str

    @field_validator("repeated_password", mode="before")
    @classmethod
    def validate_passwords_match(cls, repeated_password: str, info: ValidationInfo) -> str:
        if repeated_password != info.data.get("password"):
            raise PydanticCustomError(
                "password_mismatch",
                "passwords don't match",
            )

        return repeated_password
