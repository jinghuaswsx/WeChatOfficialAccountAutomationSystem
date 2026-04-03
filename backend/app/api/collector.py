from fastapi import APIRouter, Request

router = APIRouter(prefix="/collector")

@router.get("/scan")
async def scan_sessions(request: Request):
    from backend.app.collector.scanner import scan_sessions
    from backend.app.collector.judge import judge_publishable
    config = request.app.state.config
    sessions = scan_sessions(config.collector.claude_data_path)
    publishable = False
    for session in sessions:
        result = judge_publishable(session["messages"], min_complexity=config.collector.min_complexity)
        if result["publishable"]:
            publishable = True
            break
    return {"sessions": len(sessions), "publishable": publishable}

@router.get("/key-points")
async def list_key_points(request: Request):
    from backend.app.models.key_point import KeyPoint
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        points = db.query(KeyPoint).filter(KeyPoint.is_selected == False).all()
        return [{"id": p.id, "content": p.content, "is_selected": p.is_selected, "sanitized_content": p.sanitized_content} for p in points]
