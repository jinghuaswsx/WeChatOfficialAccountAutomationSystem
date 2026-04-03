# backend/app/api/plugins.py
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/plugins")
async def list_plugins(request: Request):
    registry = request.app.state.plugin_registry
    return registry.list_all()
