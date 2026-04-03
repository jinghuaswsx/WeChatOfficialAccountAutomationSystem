import json
from datetime import date

def test_scan_finds_todays_sessions(tmp_path):
    from backend.app.collector.scanner import scan_sessions
    project_dir = tmp_path / "projects" / "abc123" / "sessions"
    project_dir.mkdir(parents=True)
    session_file = project_dir / "session_001.jsonl"
    session_file.write_text(
        json.dumps({"type": "human", "text": "帮我实现插件系统"}) + "\n"
        + json.dumps({"type": "assistant", "text": "好的，我来实现"}) + "\n",
        encoding="utf-8",
    )
    results = scan_sessions(str(tmp_path), target_date=date(2026, 4, 4))
    assert len(results) >= 1
    assert results[0]["path"] == str(session_file)
    assert len(results[0]["messages"]) == 2

def test_scan_returns_empty_when_no_sessions(tmp_path):
    from backend.app.collector.scanner import scan_sessions
    results = scan_sessions(str(tmp_path), target_date=date(2026, 4, 4))
    assert results == []

def test_scan_skips_non_today_files(tmp_path):
    from backend.app.collector.scanner import scan_sessions
    import os, time
    project_dir = tmp_path / "projects" / "abc123" / "sessions"
    project_dir.mkdir(parents=True)
    old_file = project_dir / "old_session.jsonl"
    old_file.write_text(json.dumps({"type": "human", "text": "旧的"}) + "\n", encoding="utf-8")
    old_time = time.time() - 86400 * 30
    os.utime(str(old_file), (old_time, old_time))
    results = scan_sessions(str(tmp_path), target_date=date(2026, 4, 4))
    assert len(results) == 0
