import pytest
from backend.plugins.ai_models.mock_ai import MockAIPlugin
from backend.plugins.registry import PluginRegistry

@pytest.fixture
def registry_with_mocks():
    registry = PluginRegistry()
    registry.register_ai_model(MockAIPlugin(responses={
        "内容提炼": "# 大纲\n## 1. 项目搭建\n搭建了完整的 FastAPI 骨架\n## 2. 插件系统\n实现了四类插件",
        "文章创作": "今天花了一整天搞这个项目的骨架，说实话比想象中顺利。FastAPI 这框架确实好用...",
        "去 AI 化": "今天搞了一天项目骨架，比想的顺利不少。FastAPI 用着确实舒服...",
        "审稿": '{"approved": true, "issues": [], "suggestions": ["可以加个具体的代码示例"]}',
    }))
    return registry

@pytest.mark.asyncio
async def test_orchestrator_runs_all_stages(registry_with_mocks):
    from backend.app.pipeline.orchestrator import PipelineOrchestrator
    from backend.app.pipeline.stages import PipelineStageConfig
    stages = [
        PipelineStageConfig(name="content_extraction", plugin="mock"),
        PipelineStageConfig(name="article_writing", plugin="mock"),
        PipelineStageConfig(name="deai_processing", plugin="mock"),
        PipelineStageConfig(name="review", plugin="mock"),
    ]
    orchestrator = PipelineOrchestrator(stages=stages, registry=registry_with_mocks)
    result = await orchestrator.run(key_points=["搭建了 FastAPI 项目骨架", "实现了插件注册中心"], style_profile=None)
    assert "outline" in result
    assert "ai_draft" in result
    assert "deai_draft" in result
    assert "review_result" in result
    assert result["status"] == "completed"

@pytest.mark.asyncio
async def test_orchestrator_missing_plugin(registry_with_mocks):
    from backend.app.pipeline.orchestrator import PipelineOrchestrator
    from backend.app.pipeline.stages import PipelineStageConfig
    stages = [PipelineStageConfig(name="content_extraction", plugin="nonexistent")]
    orchestrator = PipelineOrchestrator(stages=stages, registry=registry_with_mocks)
    with pytest.raises(ValueError, match="not found"):
        await orchestrator.run(key_points=["测试"], style_profile=None)

@pytest.mark.asyncio
async def test_orchestrator_returns_intermediate_results(registry_with_mocks):
    from backend.app.pipeline.orchestrator import PipelineOrchestrator
    from backend.app.pipeline.stages import PipelineStageConfig
    stages = [
        PipelineStageConfig(name="content_extraction", plugin="mock"),
        PipelineStageConfig(name="article_writing", plugin="mock"),
    ]
    orchestrator = PipelineOrchestrator(stages=stages, registry=registry_with_mocks)
    result = await orchestrator.run(key_points=["测试要点"], style_profile=None)
    assert result["outline"] is not None
    assert result["ai_draft"] is not None
    assert result["status"] == "completed"
