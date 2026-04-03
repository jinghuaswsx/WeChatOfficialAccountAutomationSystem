def test_detect_ai_phrases():
    from backend.app.scorer.rules import detect_ai_phrases
    text = "值得注意的是，在当今数字化时代，我们需要深入探讨这个问题。总而言之，这是一次有益的尝试。"
    detected = detect_ai_phrases(text)
    assert len(detected) >= 3
    assert "值得注意的是" in detected

def test_no_ai_phrases_in_natural_text():
    from backend.app.scorer.rules import detect_ai_phrases
    text = "今天搞了一天代码，FastAPI 用着确实舒服。中间踩了个坑，SQLAlchemy 的关系映射有点绕。"
    detected = detect_ai_phrases(text)
    assert len(detected) == 0

def test_calculate_ai_trace_score():
    from backend.app.scorer.rules import calculate_ai_trace_score
    bad_text = "值得注意的是，在当今数字化时代，我们不难发现，总而言之，综上所述，这是一次有益的探索。"
    score = calculate_ai_trace_score(bad_text)
    assert score < 60
    good_text = "今天搞了一天代码。中间踩了个坑，调了半天才搞定。不过最后跑通了，挺有成就感的。"
    score = calculate_ai_trace_score(good_text)
    assert score >= 90

def test_ai_phrase_blacklist_is_comprehensive():
    from backend.app.scorer.rules import AI_PHRASE_BLACKLIST
    expected_phrases = ["值得注意的是", "总而言之", "综上所述", "不难发现"]
    for phrase in expected_phrases:
        assert phrase in AI_PHRASE_BLACKLIST
