from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from src.config.settings import settings
from src.core.dependencies.db import AsyncSessionDep

router = APIRouter(prefix="")


@router.get("/trigger-error/")
async def trigger_error() -> float:
    return 1 / 0


@router.get(
    "/health/",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def health_check(session: AsyncSessionDep) -> None:
    # Check database
    try:
        await session.execute(text("SELECT 1"))
    except (OperationalError, ConnectionRefusedError) as err:
        raise HTTPException(
            status_code=500,
            detail="Database is down",
        ) from err


@router.get(
    f"{settings.API_V1_STR}/rapidoc",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def rapidoc(request: Request) -> str:
    return f"""
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8">
                <script
                    type="module"
                    src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"
                ></script>
            </head>
            <body>
                <rapi-doc
                    spec-url="{request.app.openapi_url}"
                    header-color = "#2d87e2"
                    regular-font = "Nunito"
                    render-style = "read"
                ></rapi-doc>
            </body>
        </html>
    """
