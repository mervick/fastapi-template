from fastapi import APIRouter

from src.modules.users.routers import router as users_router

router = APIRouter(prefix="/api/v1")

router.include_router(users_router)
