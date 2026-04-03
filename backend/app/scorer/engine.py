from __future__ import annotations
from backend.app.scorer.rules import detect_ai_phrases, calculate_ai_trace_score
from backend.app.scorer.ai_scorer import get_ai_scores
from backend.plugins.base import AIModelPlugin

DEFAULT_WEIGHTS = {"content_quality": 0.3, "ai_trace": 0.3, "style_match": 0.2, "readability": 0.1, "formatting": 0.1}

class ScoreEngine:
    def __init__(self, ai_plugin: AIModelPlugin, pass_threshold: int = 80, ai_trace_hard_limit: int = 70, weights: dict[str, float] | None = None) -> None:
        self._ai_plugin = ai_plugin
        self._pass_threshold = pass_threshold
        self._ai_trace_hard_limit = ai_trace_hard_limit
        self._weights = weights or DEFAULT_WEIGHTS

    async def score(self, text: str, style_profile: dict | None = None) -> dict:
        ai_scores = await get_ai_scores(text, self._ai_plugin, style_profile)
        detected_phrases = detect_ai_phrases(text)
        rule_ai_score = calculate_ai_trace_score(text)
        dimensions = {}
        for dim, weight in self._weights.items():
            ai_s = ai_scores.get(dim, 70)
            if dim == "ai_trace":
                final = min(ai_s, rule_ai_score)
                dimensions[dim] = {"ai_score": ai_s, "rule_score": rule_ai_score, "final_score": final, "weight": weight}
            else:
                dimensions[dim] = {"ai_score": ai_s, "rule_score": None, "final_score": ai_s, "weight": weight}
        total = sum(d["final_score"] * d["weight"] for d in dimensions.values())
        fail_reasons = []
        if dimensions["ai_trace"]["final_score"] < self._ai_trace_hard_limit:
            fail_reasons.append(f"AI 痕迹分数 {dimensions['ai_trace']['final_score']} 低于硬性底线 {self._ai_trace_hard_limit}")
        if total < self._pass_threshold:
            fail_reasons.append(f"综合分 {total:.1f} 低于通过阈值 {self._pass_threshold}")
        return {"total_score": round(total, 1), "passed": len(fail_reasons) == 0, "dimensions": dimensions, "detected_ai_phrases": detected_phrases, "fail_reasons": fail_reasons}
