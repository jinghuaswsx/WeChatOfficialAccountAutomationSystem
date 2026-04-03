import json

def test_judge_publishable_with_superpowers():
    from backend.app.collector.judge import judge_publishable
    messages = [
        {"type": "human", "text": "帮我实现用户管理模块"},
        {"type": "assistant", "text": "我正在使用 brainstorming skill 来梳理需求"},
        {"type": "human", "text": "好的"},
        {"type": "assistant", "text": "我正在使用 writing-plans skill 来创建实施计划"},
        {"type": "human", "text": "继续"},
        {"type": "assistant", "text": "使用 subagent-driven-development 执行计划"},
    ]
    result = judge_publishable(messages, min_complexity="superpowers")
    assert result["publishable"] is True
    assert "superpowers" in result["reason"].lower() or "skill" in result["reason"].lower()

def test_judge_not_publishable_small_fix():
    from backend.app.collector.judge import judge_publishable
    messages = [
        {"type": "human", "text": "这个变量名写错了，帮我改一下"},
        {"type": "assistant", "text": "已修改"},
    ]
    result = judge_publishable(messages, min_complexity="superpowers")
    assert result["publishable"] is False

def test_judge_empty_messages():
    from backend.app.collector.judge import judge_publishable
    result = judge_publishable([], min_complexity="superpowers")
    assert result["publishable"] is False
