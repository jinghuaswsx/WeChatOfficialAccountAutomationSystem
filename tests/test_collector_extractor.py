import pytest
from backend.plugins.ai_models.mock_ai import MockAIPlugin

@pytest.mark.asyncio
async def test_extract_key_points():
    from backend.app.collector.extractor import extract_key_points
    mock_ai = MockAIPlugin(responses={
        "提取要点": "1. 搭建了 FastAPI 项目骨架\n2. 实现了插件注册中心\n3. 完成了数据模型设计"
    })
    messages = [
        {"type": "human", "text": "帮我搭建项目骨架"},
        {"type": "assistant", "text": "好的，我来创建 FastAPI 项目结构"},
        {"type": "human", "text": "再实现插件系统"},
        {"type": "assistant", "text": "插件注册中心已完成"},
    ]
    points = await extract_key_points(messages, ai_plugin=mock_ai)
    assert isinstance(points, list)
    assert len(points) >= 1
    for p in points:
        assert isinstance(p, str)
        assert len(p) > 0

@pytest.mark.asyncio
async def test_extract_returns_empty_for_trivial_session():
    from backend.app.collector.extractor import extract_key_points
    mock_ai = MockAIPlugin(responses={"提取要点": ""})
    messages = [{"type": "human", "text": "你好"}]
    points = await extract_key_points(messages, ai_plugin=mock_ai)
    assert points == []
