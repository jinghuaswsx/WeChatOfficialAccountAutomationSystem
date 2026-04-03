# backend/app/main.py
from pathlib import Path
from fastapi import FastAPI
from backend.app.core.config import load_config
from backend.app.core.database import create_engine_from_path, get_session_factory
from backend.app.models.base import Base
from backend.app.api.router import api_router
from backend.plugins.registry import PluginRegistry


def create_app(
    config_path: str = "config.yaml",
    db_path: str = "data/db/app.db",
) -> FastAPI:
    config = load_config(config_path)
    app = FastAPI(title="微信公众号自动化系统", version="0.1.0")

    # Database
    engine = create_engine_from_path(db_path)
    Base.metadata.create_all(engine)
    app.state.db_session_factory = get_session_factory(engine)

    # Config
    app.state.config = config

    # Plugin registry
    app.state.plugin_registry = PluginRegistry()

    # Routes
    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {"message": "微信公众号自动化系统", "version": "0.1.0"}

    return app


# For uvicorn: uvicorn backend.app.main:app
app = create_app()
