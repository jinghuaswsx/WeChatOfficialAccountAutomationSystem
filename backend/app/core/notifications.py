# backend/app/core/notifications.py
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_notification(
    event: str,
    title: str,
    details: dict | None = None,
    project: str = "WeChatAutomation",
) -> dict:
    """构建通知消息结构。"""
    return {
        "event": event,
        "title": title,
        "details": details or {},
        "project": project,
    }


def should_notify(event: str, enabled_events: list[str]) -> bool:
    """检查该事件是否应该发送通知。"""
    return event in enabled_events


def send_notification(
    title: str,
    body: str,
    project: str = "WeChatAutomation",
) -> bool:
    """
    通过 OpenClaw Notify 发送飞书通知。

    依赖本机安装的 openclaw_notify.py 脚本。
    """
    script_path = Path.home() / ".claude" / "skills" / "openclaw-notify" / "scripts" / "openclaw_notify.py"

    if not script_path.exists():
        return False

    try:
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--title", title,
                "--body", body,
                "--project", project,
                "--respect-preferences",
                "--event", "complete",
            ],
            capture_output=True,
            timeout=30,
        )
        return True
    except Exception:
        return False
