from __future__ import annotations

SUPERPOWERS_KEYWORDS = [
    "brainstorming", "writing-plans", "writing plans", "executing-plans",
    "executing plans", "subagent-driven-development", "subagent driven development",
    "test-driven-development", "superpowers",
]

def judge_publishable(messages: list[dict], min_complexity: str = "superpowers") -> dict:
    if not messages:
        return {"publishable": False, "reason": "无会话内容", "detected_skills": []}
    full_text = " ".join(m.get("text", "") for m in messages).lower()
    if min_complexity == "superpowers":
        detected = [kw for kw in SUPERPOWERS_KEYWORDS if kw in full_text]
        if detected:
            return {"publishable": True, "reason": f"检测到 Superpowers skill 使用: {', '.join(detected)}", "detected_skills": detected}
        return {"publishable": False, "reason": "未检测到 Superpowers skill 的完整使用流程", "detected_skills": []}
    return {"publishable": False, "reason": f"不支持的复杂度标准: {min_complexity}", "detected_skills": []}
