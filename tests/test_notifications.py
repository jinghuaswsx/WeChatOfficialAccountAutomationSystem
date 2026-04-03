# tests/test_notifications.py
import pytest


def test_build_notification_message():
    from backend.app.core.notifications import build_notification

    msg = build_notification(
        event="points_ready",
        title="今日有 3 个可发布要点",
        details={"count": 3},
        project="WeChatAutomation",
    )
    assert msg["title"] == "今日有 3 个可发布要点"
    assert msg["event"] == "points_ready"
    assert "project" in msg


def test_should_notify_respects_config():
    from backend.app.core.notifications import should_notify

    events = ["points_ready", "published"]
    assert should_notify("points_ready", events) is True
    assert should_notify("draft_ready", events) is False
