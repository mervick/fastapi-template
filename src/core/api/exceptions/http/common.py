from fastapi import status

from src.core.api.exceptions.http import BaseHTTPException


class PermissionDenied(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class NotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"
