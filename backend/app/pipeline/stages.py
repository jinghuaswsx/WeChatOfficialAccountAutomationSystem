from __future__ import annotations
from dataclasses import dataclass

STAGE_PROMPTS = {
    "content_extraction": "你是一名内容编辑。请根据以下要点，提炼出一篇文章的结构化大纲。\n要点列表：\n{key_points}\n\n请输出 Markdown 格式的大纲，包含标题和各段落的核心内容。",
    "article_writing": "你是一名技术博主。请根据以下大纲撰写一篇完整文章。\n{style_instruction}\n\n大纲：\n{outline}\n\n要求：\n- 用第一人称叙述\n- 语言自然，像是在和朋友分享经验\n- 包含具体的技术细节和个人感受",
    "deai_processing": "请对以下文章进行去 AI 化处理：\n1. 消除所有 AI 套话\n2. 替换机械化句式为口语化表达\n3. 增加语气词和个人化表达\n4. 打乱过于规整的段落结构\n\n原文：\n{draft}",
    "review": '请审阅以下文章，检查：\n1. 逻辑是否通顺\n2. 事实是否准确\n3. 是否有残留的 AI 痕迹\n4. 整体可读性\n\n以 JSON 格式返回：{{"approved": true/false, "issues": [...], "suggestions": [...]}}\n\n文章：\n{draft}',
}

@dataclass
class PipelineStageConfig:
    name: str
    plugin: str
