from __future__ import annotations
from backend.app.pipeline.stages import PipelineStageConfig, STAGE_PROMPTS
from backend.plugins.registry import PluginRegistry

class PipelineOrchestrator:
    def __init__(self, stages: list[PipelineStageConfig], registry: PluginRegistry) -> None:
        self._stages = stages
        self._registry = registry

    async def run(self, key_points: list[str], style_profile: dict | None) -> dict:
        result = {"outline": None, "ai_draft": None, "deai_draft": None, "review_result": None, "status": "running"}
        for stage in self._stages:
            plugin = self._registry.get_ai_model(stage.plugin)
            if plugin is None:
                raise ValueError(f"AI model plugin '{stage.plugin}' not found in registry")
            prompt = self._build_prompt(stage.name, key_points, result, style_profile)
            output = await plugin.generate(prompt)
            if stage.name == "content_extraction":
                result["outline"] = output
            elif stage.name == "article_writing":
                result["ai_draft"] = output
            elif stage.name == "deai_processing":
                result["deai_draft"] = output
            elif stage.name == "review":
                result["review_result"] = output
        result["status"] = "completed"
        return result

    def _build_prompt(self, stage_name, key_points, current_result, style_profile):
        template = STAGE_PROMPTS.get(stage_name, "{key_points}")
        style_instruction = f"写作风格要求：{style_profile}" if style_profile else ""
        return template.format(
            key_points="\n".join(f"- {p}" for p in key_points),
            outline=current_result.get("outline", ""),
            draft=current_result.get("deai_draft") or current_result.get("ai_draft", ""),
            style_instruction=style_instruction,
        )
