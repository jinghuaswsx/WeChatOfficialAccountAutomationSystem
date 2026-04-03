from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    daily_check_time: str = "20:00"


class CollectorConfig(BaseModel):
    claude_data_path: str = "~/.claude/"
    min_complexity: str = "superpowers"


class PipelineStage(BaseModel):
    name: str
    plugin: str


class PipelineConfig(BaseModel):
    stages: list[PipelineStage] = Field(default_factory=list)


class ScorerWeights(BaseModel):
    content_quality: float = 0.3
    ai_trace: float = 0.3
    style_match: float = 0.2
    readability: float = 0.1
    formatting: float = 0.1


class ScorerConfig(BaseModel):
    pass_threshold: int = 80
    ai_trace_hard_limit: int = 70
    weights: ScorerWeights = Field(default_factory=ScorerWeights)


class PublisherConfig(BaseModel):
    enabled: bool = False
    app_id: str = ""
    app_secret: str = ""


class ImageGeneratorConfig(BaseModel):
    plugin: str = "gemini"
    api_key: str = ""


class NotificationsConfig(BaseModel):
    enabled: bool = True
    engine: str = "openclaw_notify"
    events: list[str] = Field(default_factory=lambda: ["points_ready", "draft_ready", "published", "failed"])


class SystemConfig(BaseModel):
    app: AppConfig = Field(default_factory=AppConfig)
    collector: CollectorConfig = Field(default_factory=CollectorConfig)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    scorer: ScorerConfig = Field(default_factory=ScorerConfig)
    publishers: dict[str, PublisherConfig] = Field(default_factory=dict)
    image_generator: ImageGeneratorConfig = Field(default_factory=ImageGeneratorConfig)
    notifications: NotificationsConfig = Field(default_factory=NotificationsConfig)


def load_config(path: str) -> SystemConfig:
    """从 YAML 文件加载配置，缺省值由 Pydantic 模型填充。"""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return SystemConfig.model_validate(raw)
