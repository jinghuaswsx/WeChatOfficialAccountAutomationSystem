from fastapi import APIRouter, Request
from pydantic import BaseModel

class SamplesRequest(BaseModel):
    samples: list[str]

router = APIRouter(prefix="/style")

@router.get("/profile")
async def get_style_profile(request: Request):
    from backend.app.style_engine.profile import StyleProfileManager
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        manager = StyleProfileManager(db)
        profile = manager.get_latest()
        return {"profile": profile}

@router.post("/samples")
async def upload_samples(req: SamplesRequest):
    return {"status": "accepted", "count": len(req.samples)}
