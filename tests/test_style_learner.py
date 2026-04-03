import pytest
from backend.plugins.ai_models.mock_ai import MockAIPlugin

@pytest.mark.asyncio
async def test_analyze_style_from_samples():
    from backend.app.style_engine.analyzer import analyze_style
    mock_ai = MockAIPlugin(responses={
        "风格分析": '{"vocabulary": {"preferred_words": ["搞定"], "tone": "口语化"}, "sentence_patterns": {"avg_length": 15}}'
    })
    samples = ["今天搞了一天代码，踩了不少坑。", "这个功能折腾了半天，总算搞定了。"]
    features = await analyze_style(samples, ai_plugin=mock_ai)
    assert "vocabulary" in features
    assert "sentence_patterns" in features

@pytest.mark.asyncio
async def test_learn_from_revision():
    from backend.app.style_engine.learner import learn_from_revision
    mock_ai = MockAIPlugin(responses={
        "修改分析": '{"commonly_deleted": ["值得注意的是"], "commonly_rewritten": [{"from": "进行了探讨", "to": "聊了聊"}], "style_shifts": ["更口语化"]}'
    })
    ai_draft = "值得注意的是，我们今天进行了探讨。这是一次有益的尝试。"
    user_final = "今天聊了聊这个事。试了一下还不错。"
    patterns = await learn_from_revision(ai_draft, user_final, ai_plugin=mock_ai)
    assert "commonly_deleted" in patterns or "style_shifts" in patterns
