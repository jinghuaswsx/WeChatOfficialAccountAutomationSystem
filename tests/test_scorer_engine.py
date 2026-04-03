import pytest
from backend.plugins.ai_models.mock_ai import MockAIPlugin

@pytest.mark.asyncio
async def test_score_article_passes():
    from backend.app.scorer.engine import ScoreEngine
    mock_ai = MockAIPlugin(responses={
        "评分": '{"content_quality": 85, "ai_trace": 90, "style_match": 80, "readability": 85, "formatting": 90}'
    })
    engine = ScoreEngine(ai_plugin=mock_ai, pass_threshold=80, ai_trace_hard_limit=70)
    text = "今天搞了一天代码。中间踩了个坑，调了半天才搞定。"
    result = await engine.score(text, style_profile=None)
    assert result["passed"] is True
    assert result["total_score"] >= 80
    assert "dimensions" in result

@pytest.mark.asyncio
async def test_score_article_fails_ai_trace():
    from backend.app.scorer.engine import ScoreEngine
    mock_ai = MockAIPlugin(responses={
        "评分": '{"content_quality": 90, "ai_trace": 90, "style_match": 85, "readability": 85, "formatting": 90}'
    })
    engine = ScoreEngine(ai_plugin=mock_ai, pass_threshold=80, ai_trace_hard_limit=70)
    text = "值得注意的是，在当今数字化时代，我们需要深入探讨这个问题。综上所述，总而言之，不难发现，这是一次有益的探索。毋庸置疑，众所周知，这不可或缺。"
    result = await engine.score(text, style_profile=None)
    assert result["dimensions"]["ai_trace"]["rule_score"] < 70

@pytest.mark.asyncio
async def test_score_returns_suggestions():
    from backend.app.scorer.engine import ScoreEngine
    mock_ai = MockAIPlugin(responses={
        "评分": '{"content_quality": 75, "ai_trace": 80, "style_match": 70, "readability": 75, "formatting": 80}'
    })
    engine = ScoreEngine(ai_plugin=mock_ai, pass_threshold=80, ai_trace_hard_limit=70)
    text = "今天写了点代码。"
    result = await engine.score(text, style_profile=None)
    assert "detected_ai_phrases" in result
