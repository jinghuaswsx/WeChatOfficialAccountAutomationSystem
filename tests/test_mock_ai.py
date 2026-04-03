import pytest

@pytest.mark.asyncio
async def test_mock_ai_generate():
    from backend.plugins.ai_models.mock_ai import MockAIPlugin
    plugin = MockAIPlugin()
    result = await plugin.generate("你好")
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mock_ai_with_custom_response():
    from backend.plugins.ai_models.mock_ai import MockAIPlugin
    plugin = MockAIPlugin(responses={"提取要点": "1. 实现了插件系统\n2. 搭建了 FastAPI"})
    result = await plugin.generate("提取要点")
    assert "插件系统" in result

def test_mock_ai_name():
    from backend.plugins.ai_models.mock_ai import MockAIPlugin
    plugin = MockAIPlugin()
    assert plugin.name == "mock"

def test_mock_ai_is_ai_model_plugin():
    from backend.plugins.ai_models.mock_ai import MockAIPlugin
    from backend.plugins.base import AIModelPlugin
    plugin = MockAIPlugin()
    assert isinstance(plugin, AIModelPlugin)
