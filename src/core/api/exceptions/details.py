from dataclasses import dataclass


@dataclass(frozen=True)
class ExceptionDetail:
    # NOTE: bad request
    unique_value: str = "duplicated value for field {field_name}"
