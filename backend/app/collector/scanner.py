from __future__ import annotations
import json
from datetime import date, datetime
from pathlib import Path

def scan_sessions(claude_data_path: str, target_date: date | None = None) -> list[dict]:
    if target_date is None:
        target_date = date.today()
    base = Path(claude_data_path)
    results = []
    projects_dir = base / "projects"
    if not projects_dir.exists():
        return results
    for session_file in projects_dir.rglob("*.jsonl"):
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime).date()
        if mtime != target_date:
            continue
        messages = _parse_session_file(session_file)
        if messages:
            results.append({"path": str(session_file), "messages": messages})
    return results

def _parse_session_file(path: Path) -> list[dict]:
    messages = []
    try:
        for line in path.read_text(encoding="utf-8").strip().splitlines():
            line = line.strip()
            if line:
                messages.append(json.loads(line))
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    return messages
