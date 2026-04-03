from __future__ import annotations
import json
from backend.plugins.base import AIModelPlugin

ANALYZE_PROMPT = """请分析以下文章样本的写作风格特征。

样本文章：
{samples}

请以 JSON 格式返回风格特征，包含：
- vocabulary: 词汇偏好
- sentence_patterns: 句式特征
- structure: 文章结构特征

只返回 JSON："""

async def analyze_style(samples: list[str], ai_plugin: AIModelPlugin) -> dict:
    samples_text = "\n\n---\n\n".join(samples)
    prompt = ANALYZE_PROMPT.format(samples=samples_text)
    raw = await ai_plugin.generate(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"vocabulary": {}, "sentence_patterns": {}, "structure": {}}
