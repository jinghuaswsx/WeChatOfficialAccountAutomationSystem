import os
import tempfile
from pathlib import Path

import yaml


def test_load_config_from_yaml(tmp_path):
    """从 YAML 文件加载配置"""
    config_data = {
        "app": {"host": "127.0.0.1", "port": 8000, "daily_check_time": "20:00"},
        "collector": {
            "claude_data_path": "~/.claude/",
            "min_complexity": "superpowers",
        },
        "pipeline": {
            "stages": [
                {"name": "content_extraction", "plugin": "claude"},
                {"name": "article_writing", "plugin": "deepseek"},
            ]
        },
        "scorer": {
            "pass_threshold": 80,
            "ai_trace_hard_limit": 70,
            "weights": {
                "content_quality": 0.3,
                "ai_trace": 0.3,
                "style_match": 0.2,
                "readability": 0.1,
                "formatting": 0.1,
            },
        },
        "publishers": {"wechat": {"enabled": True, "app_id": "test", "app_secret": "secret"}},
        "image_generator": {"plugin": "gemini", "api_key": "test-key"},
        "notifications": {
            "enabled": True,
            "engine": "openclaw_notify",
            "events": ["points_ready", "published"],
        },
    }
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data, allow_unicode=True))

    from backend.app.core.config import load_config

    config = load_config(str(config_file))

    assert config.app.host == "127.0.0.1"
    assert config.app.port == 8000
    assert config.scorer.pass_threshold == 80
    assert config.scorer.weights.content_quality == 0.3
    assert config.publishers["wechat"].enabled is True
    assert len(config.pipeline.stages) == 2


def test_load_config_defaults(tmp_path):
    """缺省值正确填充"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump({"app": {}}, allow_unicode=True))

    from backend.app.core.config import load_config

    config = load_config(str(config_file))

    assert config.app.host == "127.0.0.1"
    assert config.app.port == 8000
    assert config.app.daily_check_time == "20:00"
    assert config.scorer.pass_threshold == 80


def test_load_config_file_not_found():
    """配置文件不存在时抛出 FileNotFoundError"""
    from backend.app.core.config import load_config
    import pytest

    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml")
