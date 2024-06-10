from typing import Annotated

from fastapi import HTTPException
from typing_extensions import Doc


class BaseHTTPException(HTTPException):
    def __init__(
        self,
        detail: Annotated[
            str | None,
            Doc(
                """
                Any data to be sent to the client in the `detail` key of the JSON
                response.
                """
            ),
        ] = None,
        status_code: Annotated[
            int | None,
            Doc(
                """
                HTTP status code to send to the client.
                """
            ),
        ] = None,
        headers: Annotated[
            dict[str, str] | None,
            Doc(
                """
                Any headers to send to the client in the response.
                """
            ),
        ] = None,
    ) -> None:
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code, detail, headers)
