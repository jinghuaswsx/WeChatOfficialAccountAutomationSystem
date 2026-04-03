from __future__ import annotations
import json
from backend.plugins.base import AIModelPlugin

REVISION_ANALYSIS_PROMPT = """请对比以下两个版本的文章，分析用户的修改偏好：

AI 原稿：
{ai_draft}

用户修改后：
{user_final}

请分析修改模式：
- commonly_deleted: 用户删除的常见表达
- commonly_rewritten: 常见改写模式
- style_shifts: 整体风格转变

以 JSON 格式返回，只返回 JSON："""

async def learn_from_revision(ai_draft: str, user_final: str, ai_plugin: AIModelPlugin) -> dict:
    prompt = REVISION_ANALYSIS_PROMPT.format(ai_draft=ai_draft, user_final=user_final)
    raw = await ai_plugin.generate(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"commonly_deleted": [], "commonly_rewritten": [], "style_shifts": []}
