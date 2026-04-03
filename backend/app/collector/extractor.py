from __future__ import annotations
from backend.plugins.base import AIModelPlugin

EXTRACT_PROMPT_TEMPLATE = """任务：提取要点。
请从以下 Claude Code 对话记录中提取核心要点。
每个要点应描述：解决了什么问题、用了什么方法、做了什么关键决策。
每行一个要点，不要加编号前缀。如果对话过于简短或无实质内容，返回空。

对话记录：
{conversation}
"""

async def extract_key_points(messages: list[dict], ai_plugin: AIModelPlugin) -> list[str]:
    conversation = "\n".join(
        f"{'用户' if m.get('type') == 'human' else 'AI'}: {m.get('text', '')}"
        for m in messages
    )
    prompt = EXTRACT_PROMPT_TEMPLATE.format(conversation=conversation)
    result = await ai_plugin.generate(prompt)
    return _parse_points(result)

def _parse_points(raw: str) -> list[str]:
    if not raw or not raw.strip():
        return []
    points = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if line and len(line) > 1:
            cleaned = line.lstrip("0123456789.-) ").strip()
            if cleaned:
                points.append(cleaned)
    return points
