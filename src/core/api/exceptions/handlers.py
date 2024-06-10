from asyncpg.exceptions import TooManyConnectionsError, UniqueViolationError
from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import IntegrityError


async def unique_violation_error_handler(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    _ = request

    if exc.orig is None or exc.orig.__cause__ is None:
        raise exc

    if not isinstance(exc.orig.__cause__, UniqueViolationError):
        raise exc

    # here inside exc_details we have key "detail" and value:
    #     "Key (field_name)=(value) already exists."
    # I need to extract field_name from exc_details["detail"]
    exc_details = exc.orig.__cause__.as_dict()
    field_name = exc_details["detail"].replace("Key (", "").split(")=(")[0]

    content = {
        "detail": [
            {
                "type": "unique_validation_error",
                "msg": "duplicated value for field",
                "loc": ["body", field_name],
            }
        ]
    }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )


async def database_too_many_connections_error_handler(
    request: Request,
    exc: TooManyConnectionsError,
) -> JSONResponse:
    _ = request

    logger.error(exc.as_dict())
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Service temporarily unavailable. Please try again later.",
        },
        headers={"Retry-After": "5"},
    )
