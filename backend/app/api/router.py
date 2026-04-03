# backend/app/api/router.py
from fastapi import APIRouter
from backend.app.api.health import router as health_router
from backend.app.api.plugins import router as plugins_router
from backend.app.api.collector import router as collector_router
from backend.app.api.pipeline import router as pipeline_router
from backend.app.api.scorer import router as scorer_router
from backend.app.api.style import router as style_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(plugins_router)
api_router.include_router(collector_router)
api_router.include_router(pipeline_router)
api_router.include_router(scorer_router)
api_router.include_router(style_router)
