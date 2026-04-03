from __future__ import annotations

AI_PHRASE_BLACKLIST = [
    "在当今", "随着科技的发展", "随着技术的不断进步", "在数字化时代", "在这个信息爆炸的时代",
    "值得注意的是", "不难发现", "众所周知", "毋庸置疑", "不可否认", "事实上", "显而易见", "毫无疑问",
    "总而言之", "综上所述", "总的来说", "归根结底",
    "深入探讨", "全面分析", "有益的探索", "有益的尝试", "宝贵的经验", "至关重要", "不可或缺",
    "赋能", "助力", "驱动", "引领", "打造", "构建", "携手", "共创",
    "让我们一起", "希望本文能够", "相信在不远的将来", "期待未来",
]

def detect_ai_phrases(text: str) -> list[str]:
    return [phrase for phrase in AI_PHRASE_BLACKLIST if phrase in text]

def calculate_ai_trace_score(text: str) -> int:
    detected = detect_ai_phrases(text)
    penalty = len(detected) * 8
    return max(0, 100 - penalty)
