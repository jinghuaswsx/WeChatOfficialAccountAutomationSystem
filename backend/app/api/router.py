# backend/app/api/router.py
from fastapi import APIRouter
from backend.app.api.health import router as health_router
from backend.app.api.plugins import router as plugins_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(plugins_router)
