from fastapi import APIRouter

__all__ = ("router",)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
