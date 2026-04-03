from __future__ import annotations
import json
from backend.plugins.base import AIModelPlugin

SCORE_PROMPT = """请对以下文章进行多维度评分 (0-100)：
评分维度：
- content_quality: 内容质量
- ai_trace: AI 痕迹（越少分越高）
- style_match: 文风匹配度
- readability: 可读性
- formatting: 排版规范

{style_context}

文章：
{text}

只返回 JSON：
{{"content_quality": 分数, "ai_trace": 分数, "style_match": 分数, "readability": 分数, "formatting": 分数}}"""

async def get_ai_scores(text: str, ai_plugin: AIModelPlugin, style_profile: dict | None = None) -> dict[str, int]:
    style_context = f"参考文风画像：{style_profile}" if style_profile else ""
    prompt = SCORE_PROMPT.format(text=text, style_context=style_context)
    raw = await ai_plugin.generate(prompt)
    try:
        scores = json.loads(raw)
        return {k: int(scores.get(k, 70)) for k in ["content_quality", "ai_trace", "style_match", "readability", "formatting"]}
    except (json.JSONDecodeError, ValueError):
        return {k: 70 for k in ["content_quality", "ai_trace", "style_match", "readability", "formatting"]}
