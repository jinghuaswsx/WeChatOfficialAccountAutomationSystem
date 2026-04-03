from fastapi import APIRouter

router = APIRouter(prefix="/pipeline")
_pipeline_state = {"status": "idle", "current_stage": None, "result": None}

@router.get("/status")
async def pipeline_status():
    return _pipeline_state
