from fastapi import APIRouter, Request
from pydantic import BaseModel

class ScoreRequest(BaseModel):
    text: str

router = APIRouter(prefix="/scorer")

@router.post("/score")
async def score_article(req: ScoreRequest, request: Request):
    from backend.app.scorer.engine import ScoreEngine
    from backend.plugins.ai_models.mock_ai import MockAIPlugin
    config = request.app.state.config
    registry = request.app.state.plugin_registry
    ai_plugin = registry.get_ai_model("scorer") or registry.get_ai_model("mock") or MockAIPlugin()
    engine = ScoreEngine(
        ai_plugin=ai_plugin,
        pass_threshold=config.scorer.pass_threshold,
        ai_trace_hard_limit=config.scorer.ai_trace_hard_limit,
        weights={
            "content_quality": config.scorer.weights.content_quality,
            "ai_trace": config.scorer.weights.ai_trace,
            "style_match": config.scorer.weights.style_match,
            "readability": config.scorer.weights.readability,
            "formatting": config.scorer.weights.formatting,
        },
    )
    result = await engine.score(req.text)
    return result
