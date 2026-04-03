# Plan 1: 基础骨架 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 搭建项目基础骨架，包括 FastAPI 服务、插件注册中心、数据库模型、配置系统，使后续模块可以在此基础上插件化接入。

**Architecture:** 插件式单体架构。FastAPI 为核心框架，SQLAlchemy + SQLite 做数据持久化，YAML 配置文件驱动插件加载。插件注册中心通过基类约束 + 自动发现机制管理所有插件。

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, PyYAML, pytest, uv

---

## File Structure

```
WeChatOfficialAccountAutomationSystem/
├── pyproject.toml                          # 项目元数据和依赖
├── config.yaml                             # 运行时配置
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                         # FastAPI 应用入口
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py                   # 配置加载与校验
│   │   │   └── database.py                 # 数据库引擎与会话管理
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py                   # 总路由聚合
│   │   │   ├── health.py                   # 健康检查端点
│   │   │   └── plugins.py                  # 插件管理端点
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── base.py                     # SQLAlchemy Base
│   │       ├── session.py                  # Session 模型
│   │       ├── key_point.py                # KeyPoint 模型
│   │       ├── article.py                  # Article 模型
│   │       ├── style_profile.py            # StyleProfile 模型
│   │       └── revision_history.py         # RevisionHistory 模型
│   └── plugins/
│       ├── __init__.py
│       ├── base.py                         # 四类插件基类
│       └── registry.py                     # 插件注册中心
├── tests/
│   ├── __init__.py
│   ├── conftest.py                         # pytest fixtures
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_plugin_base.py
│   ├── test_plugin_registry.py
│   ├── test_api_health.py
│   └── test_api_plugins.py
└── data/
    ├── style_samples/                      # 文风样本目录（空，预留）
    └── db/                                 # SQLite 数据库目录
```

---

## Task 1: 项目初始化与依赖安装

**Files:**
- Create: `pyproject.toml`
- Create: `backend/app/__init__.py`
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/plugins/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: 创建 pyproject.toml**

```toml
[project]
name = "wechat-automation"
version = "0.1.0"
description = "微信公众号自动化系统"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "pyyaml>=6.0",
    "aiosqlite>=0.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 2: 创建所有 `__init__.py` 空文件**

创建以下空文件：
- `backend/app/__init__.py`
- `backend/app/core/__init__.py`
- `backend/app/api/__init__.py`
- `backend/app/models/__init__.py`
- `backend/plugins/__init__.py`
- `tests/__init__.py`

- [ ] **Step 3: 创建 data 目录**

```bash
mkdir -p data/style_samples data/db
```

- [ ] **Step 4: 安装依赖**

```bash
uv pip install -e ".[dev]"
```

如果没有 uv，退回到：
```bash
pip install -e ".[dev]"
```

- [ ] **Step 5: 验证安装**

Run: `python -c "import fastapi; import sqlalchemy; import pydantic; print('OK')"`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml backend/ tests/ data/
git commit -m "chore: 项目初始化，配置依赖和目录结构"
```

---

## Task 2: 配置系统

**Files:**
- Create: `config.yaml`
- Create: `backend/app/core/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: 写配置加载的 failing test**

```python
# tests/test_config.py
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'backend.app.core.config'`

- [ ] **Step 3: 实现配置模块**

```python
# backend/app/core/config.py
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_config.py -v`
Expected: 3 passed

- [ ] **Step 5: 创建默认 config.yaml**

```yaml
# config.yaml
app:
  host: "127.0.0.1"
  port: 8000
  daily_check_time: "20:00"

collector:
  claude_data_path: "~/.claude/"
  min_complexity: "superpowers"

pipeline:
  stages:
    - name: "content_extraction"
      plugin: "claude"
    - name: "article_writing"
      plugin: "deepseek"
    - name: "deai_processing"
      plugin: "qwen"
    - name: "review"
      plugin: "claude"

scorer:
  pass_threshold: 80
  ai_trace_hard_limit: 70
  weights:
    content_quality: 0.3
    ai_trace: 0.3
    style_match: 0.2
    readability: 0.1
    formatting: 0.1

publishers:
  wechat:
    enabled: true
    app_id: ""
    app_secret: ""
  xiaohongshu:
    enabled: false
  twitter:
    enabled: false

image_generator:
  plugin: "gemini"
  api_key: ""

notifications:
  enabled: true
  engine: "openclaw_notify"
  events:
    - "points_ready"
    - "draft_ready"
    - "published"
    - "failed"
```

- [ ] **Step 6: Commit**

```bash
git add config.yaml backend/app/core/config.py tests/test_config.py
git commit -m "feat: 配置系统，YAML 加载 + Pydantic 校验"
```

---

## Task 3: 数据库引擎与会话管理

**Files:**
- Create: `backend/app/core/database.py`
- Create: `tests/test_database.py`

- [ ] **Step 1: 写数据库引擎的 failing test**

```python
# tests/test_database.py
import pytest
from sqlalchemy import text


@pytest.fixture
def db_engine(tmp_path):
    from backend.app.core.database import create_engine_from_path

    db_path = tmp_path / "test.db"
    engine = create_engine_from_path(str(db_path))
    return engine


def test_create_engine(db_engine):
    """能创建 SQLite 引擎并连接"""
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_session(db_engine):
    """能获取数据库会话"""
    from backend.app.core.database import get_session_factory

    SessionFactory = get_session_factory(db_engine)
    with SessionFactory() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_database.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 实现数据库模块**

```python
# backend/app/core/database.py
from pathlib import Path

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


def create_engine_from_path(db_path: str) -> Engine:
    """根据文件路径创建 SQLite 引擎。"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{db_path}", echo=False)


def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    """创建绑定到指定引擎的 Session 工厂。"""
    return sessionmaker(bind=engine)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_database.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add backend/app/core/database.py tests/test_database.py
git commit -m "feat: 数据库引擎与会话工厂"
```

---

## Task 4: 数据模型

**Files:**
- Create: `backend/app/models/base.py`
- Create: `backend/app/models/session.py`
- Create: `backend/app/models/key_point.py`
- Create: `backend/app/models/article.py`
- Create: `backend/app/models/style_profile.py`
- Create: `backend/app/models/revision_history.py`
- Create: `backend/app/models/__init__.py` (更新)
- Create: `tests/test_models.py`

- [ ] **Step 1: 写模型的 failing test**

```python
# tests/test_models.py
import pytest
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.models.base import Base
from backend.app.models.session import SessionRecord
from backend.app.models.key_point import KeyPoint
from backend.app.models.article import Article
from backend.app.models.style_profile import StyleProfile
from backend.app.models.revision_history import RevisionHistory


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_session_record(db_session):
    """创建 SessionRecord 并持久化"""
    record = SessionRecord(
        session_date=date(2026, 4, 4),
        source_path="/home/user/.claude/sessions/abc123",
        extraction_status="pending",
    )
    db_session.add(record)
    db_session.commit()

    loaded = db_session.get(SessionRecord, record.id)
    assert loaded is not None
    assert loaded.session_date == date(2026, 4, 4)
    assert loaded.extraction_status == "pending"


def test_create_key_point_linked_to_session(db_session):
    """KeyPoint 关联到 SessionRecord"""
    record = SessionRecord(
        session_date=date(2026, 4, 4),
        source_path="/path/to/session",
        extraction_status="done",
    )
    db_session.add(record)
    db_session.flush()

    kp = KeyPoint(
        session_id=record.id,
        content="实现了插件注册中心",
        is_selected=False,
        sanitized_content=None,
    )
    db_session.add(kp)
    db_session.commit()

    loaded = db_session.get(KeyPoint, kp.id)
    assert loaded.content == "实现了插件注册中心"
    assert loaded.session_id == record.id


def test_article_status_flow(db_session):
    """Article 状态字段正确存储"""
    article = Article(
        title="测试文章",
        status="extracting",
        outline=None,
        ai_draft=None,
        deai_draft=None,
        final_draft=None,
        score=None,
        published_at=None,
    )
    db_session.add(article)
    db_session.commit()

    article.status = "published"
    db_session.commit()

    loaded = db_session.get(Article, article.id)
    assert loaded.status == "published"


def test_style_profile(db_session):
    """StyleProfile 存储 JSON 特征"""
    import json

    features = {"vocabulary": {"preferred_words": ["搞定"]}}
    profile = StyleProfile(
        version=1,
        features_json=json.dumps(features, ensure_ascii=False),
    )
    db_session.add(profile)
    db_session.commit()

    loaded = db_session.get(StyleProfile, profile.id)
    parsed = json.loads(loaded.features_json)
    assert parsed["vocabulary"]["preferred_words"] == ["搞定"]


def test_revision_history(db_session):
    """RevisionHistory 存储 AI 原稿和用户终稿"""
    article = Article(title="测试", status="draft_ready")
    db_session.add(article)
    db_session.flush()

    revision = RevisionHistory(
        article_id=article.id,
        ai_draft="AI 写的内容",
        user_final="用户改后的内容",
        diff_summary="删除了3处AI套话",
    )
    db_session.add(revision)
    db_session.commit()

    loaded = db_session.get(RevisionHistory, revision.id)
    assert loaded.ai_draft == "AI 写的内容"
    assert loaded.article_id == article.id
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 实现 Base**

```python
# backend/app/models/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

- [ ] **Step 4: 实现 SessionRecord 模型**

```python
# backend/app/models/session.py
from datetime import date, datetime

from sqlalchemy import Integer, String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class SessionRecord(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_date: Mapped[date] = mapped_column(Date, nullable=False)
    source_path: Mapped[str] = mapped_column(String, nullable=False)
    extraction_status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    key_points: Mapped[list["KeyPoint"]] = relationship(back_populates="session")
```

- [ ] **Step 5: 实现 KeyPoint 模型**

```python
# backend/app/models/key_point.py
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class KeyPoint(Base):
    __tablename__ = "key_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_selected: Mapped[bool] = mapped_column(Boolean, default=False)
    sanitized_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["SessionRecord"] = relationship(back_populates="key_points")
```

- [ ] **Step 6: 实现 Article 模型**

```python
# backend/app/models/article.py
from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="extracting")
    outline: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_draft: Mapped[str | None] = mapped_column(Text, nullable=True)
    deai_draft: Mapped[str | None] = mapped_column(Text, nullable=True)
    final_draft: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    revisions: Mapped[list["RevisionHistory"]] = relationship(back_populates="article")
```

- [ ] **Step 7: 实现 StyleProfile 模型**

```python
# backend/app/models/style_profile.py
from datetime import datetime

from sqlalchemy import Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class StyleProfile(Base):
    __tablename__ = "style_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    features_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

- [ ] **Step 8: 实现 RevisionHistory 模型**

```python
# backend/app/models/revision_history.py
from datetime import datetime

from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class RevisionHistory(Base):
    __tablename__ = "revision_histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id"), nullable=False)
    ai_draft: Mapped[str] = mapped_column(Text, nullable=False)
    user_final: Mapped[str] = mapped_column(Text, nullable=False)
    diff_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    article: Mapped["Article"] = relationship(back_populates="revisions")
```

- [ ] **Step 9: 更新 models `__init__.py` 导出所有模型**

```python
# backend/app/models/__init__.py
from backend.app.models.base import Base
from backend.app.models.session import SessionRecord
from backend.app.models.key_point import KeyPoint
from backend.app.models.article import Article
from backend.app.models.style_profile import StyleProfile
from backend.app.models.revision_history import RevisionHistory

__all__ = [
    "Base",
    "SessionRecord",
    "KeyPoint",
    "Article",
    "StyleProfile",
    "RevisionHistory",
]
```

- [ ] **Step 10: 运行测试确认通过**

Run: `pytest tests/test_models.py -v`
Expected: 5 passed

- [ ] **Step 11: Commit**

```bash
git add backend/app/models/ tests/test_models.py
git commit -m "feat: 数据模型 — Session, KeyPoint, Article, StyleProfile, RevisionHistory"
```

---

## Task 5: 插件基类

**Files:**
- Create: `backend/plugins/base.py`
- Create: `tests/test_plugin_base.py`

- [ ] **Step 1: 写插件基类的 failing test**

```python
# tests/test_plugin_base.py
import pytest
from abc import ABC


def test_ai_model_plugin_is_abstract():
    """AIModelPlugin 不能直接实例化"""
    from backend.plugins.base import AIModelPlugin

    with pytest.raises(TypeError):
        AIModelPlugin()


def test_publisher_plugin_is_abstract():
    """PublisherPlugin 不能直接实例化"""
    from backend.plugins.base import PublisherPlugin

    with pytest.raises(TypeError):
        PublisherPlugin()


def test_formatter_plugin_is_abstract():
    """FormatterPlugin 不能直接实例化"""
    from backend.plugins.base import FormatterPlugin

    with pytest.raises(TypeError):
        FormatterPlugin()


def test_image_generator_plugin_is_abstract():
    """ImageGeneratorPlugin 不能直接实例化"""
    from backend.plugins.base import ImageGeneratorPlugin

    with pytest.raises(TypeError):
        ImageGeneratorPlugin()


def test_concrete_ai_model_plugin():
    """具体 AI 模型插件可以实例化"""
    from backend.plugins.base import AIModelPlugin

    class MockAI(AIModelPlugin):
        @property
        def name(self) -> str:
            return "mock"

        async def generate(self, prompt: str, **kwargs) -> str:
            return "mock response"

    plugin = MockAI()
    assert plugin.name == "mock"


def test_concrete_publisher_plugin():
    """具体发布插件可以实例化"""
    from backend.plugins.base import PublisherPlugin

    class MockPublisher(PublisherPlugin):
        @property
        def name(self) -> str:
            return "mock"

        @property
        def platform(self) -> str:
            return "mock_platform"

        async def authenticate(self) -> bool:
            return True

        async def upload_image(self, image_path: str) -> str:
            return "url"

        async def create_draft(self, title: str, content: str, images: list[str]) -> str:
            return "draft_id"

        async def publish(self, draft_id: str) -> bool:
            return True

        async def get_publish_status(self, draft_id: str) -> str:
            return "published"

    plugin = MockPublisher()
    assert plugin.platform == "mock_platform"


def test_concrete_formatter_plugin():
    """具体排版插件可以实例化"""
    from backend.plugins.base import FormatterPlugin

    class MockFormatter(FormatterPlugin):
        @property
        def name(self) -> str:
            return "mock"

        @property
        def platform(self) -> str:
            return "mock_platform"

        def format(self, markdown: str, images: list[str] | None = None) -> str:
            return f"<p>{markdown}</p>"

    plugin = MockFormatter()
    assert plugin.format("hello") == "<p>hello</p>"


def test_concrete_image_generator_plugin():
    """具体图片生成插件可以实例化"""
    from backend.plugins.base import ImageGeneratorPlugin

    class MockImageGen(ImageGeneratorPlugin):
        @property
        def name(self) -> str:
            return "mock"

        async def generate(self, prompt: str, **kwargs) -> str:
            return "/path/to/image.png"

    plugin = MockImageGen()
    assert plugin.name == "mock"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_plugin_base.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 实现四类插件基类**

```python
# backend/plugins/base.py
from abc import ABC, abstractmethod


class PluginBase(ABC):
    """所有插件的根基类。"""

    @property
    @abstractmethod
    def name(self) -> str:
        """插件唯一标识名。"""
        ...


class AIModelPlugin(PluginBase):
    """AI 模型插件基类。用于写作流水线各阶段。"""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """根据 prompt 生成文本。"""
        ...


class PublisherPlugin(PluginBase):
    """发布平台插件基类。"""

    @property
    @abstractmethod
    def platform(self) -> str:
        """平台标识（如 wechat, xiaohongshu, twitter）。"""
        ...

    @abstractmethod
    async def authenticate(self) -> bool: ...

    @abstractmethod
    async def upload_image(self, image_path: str) -> str: ...

    @abstractmethod
    async def create_draft(self, title: str, content: str, images: list[str]) -> str: ...

    @abstractmethod
    async def publish(self, draft_id: str) -> bool: ...

    @abstractmethod
    async def get_publish_status(self, draft_id: str) -> str: ...


class FormatterPlugin(PluginBase):
    """排版引擎插件基类。将 Markdown 转为平台特定格式。"""

    @property
    @abstractmethod
    def platform(self) -> str:
        """目标平台标识。"""
        ...

    @abstractmethod
    def format(self, markdown: str, images: list[str] | None = None) -> str:
        """将 Markdown 转为平台特定的富文本/HTML。"""
        ...


class ImageGeneratorPlugin(PluginBase):
    """图片生成插件基类。"""

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """根据 prompt 生成图片，返回本地文件路径。"""
        ...
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_plugin_base.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add backend/plugins/base.py tests/test_plugin_base.py
git commit -m "feat: 四类插件基类 — AIModel, Publisher, Formatter, ImageGenerator"
```

---

## Task 6: 插件注册中心

**Files:**
- Create: `backend/plugins/registry.py`
- Create: `tests/test_plugin_registry.py`

- [ ] **Step 1: 写注册中心的 failing test**

```python
# tests/test_plugin_registry.py
import pytest

from backend.plugins.base import AIModelPlugin, PublisherPlugin, FormatterPlugin, ImageGeneratorPlugin


# -- 测试用的 mock 插件 --

class FakeAI(AIModelPlugin):
    @property
    def name(self) -> str:
        return "fake_ai"

    async def generate(self, prompt: str, **kwargs) -> str:
        return "fake"


class FakePublisher(PublisherPlugin):
    @property
    def name(self) -> str:
        return "fake_pub"

    @property
    def platform(self) -> str:
        return "fake"

    async def authenticate(self) -> bool:
        return True

    async def upload_image(self, image_path: str) -> str:
        return "url"

    async def create_draft(self, title: str, content: str, images: list[str]) -> str:
        return "draft"

    async def publish(self, draft_id: str) -> bool:
        return True

    async def get_publish_status(self, draft_id: str) -> str:
        return "ok"


class FakeFormatter(FormatterPlugin):
    @property
    def name(self) -> str:
        return "fake_fmt"

    @property
    def platform(self) -> str:
        return "fake"

    def format(self, markdown: str, images: list[str] | None = None) -> str:
        return markdown


class FakeImageGen(ImageGeneratorPlugin):
    @property
    def name(self) -> str:
        return "fake_img"

    async def generate(self, prompt: str, **kwargs) -> str:
        return "/fake.png"


# -- 测试 --

def test_register_and_get_ai_model():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    plugin = FakeAI()
    registry.register_ai_model(plugin)

    assert registry.get_ai_model("fake_ai") is plugin


def test_register_and_get_publisher():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    plugin = FakePublisher()
    registry.register_publisher(plugin)

    assert registry.get_publisher("fake_pub") is plugin


def test_register_and_get_formatter():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    plugin = FakeFormatter()
    registry.register_formatter(plugin)

    assert registry.get_formatter("fake_fmt") is plugin


def test_register_and_get_image_generator():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    plugin = FakeImageGen()
    registry.register_image_generator(plugin)

    assert registry.get_image_generator("fake_img") is plugin


def test_get_nonexistent_plugin_returns_none():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    assert registry.get_ai_model("nonexistent") is None


def test_list_plugins():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    registry.register_ai_model(FakeAI())
    registry.register_publisher(FakePublisher())
    registry.register_formatter(FakeFormatter())
    registry.register_image_generator(FakeImageGen())

    all_plugins = registry.list_all()
    assert all_plugins == {
        "ai_models": ["fake_ai"],
        "publishers": ["fake_pub"],
        "formatters": ["fake_fmt"],
        "image_generators": ["fake_img"],
    }


def test_duplicate_register_raises():
    from backend.plugins.registry import PluginRegistry

    registry = PluginRegistry()
    registry.register_ai_model(FakeAI())

    with pytest.raises(ValueError, match="already registered"):
        registry.register_ai_model(FakeAI())
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_plugin_registry.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 实现插件注册中心**

```python
# backend/plugins/registry.py
from __future__ import annotations

from backend.plugins.base import (
    AIModelPlugin,
    PublisherPlugin,
    FormatterPlugin,
    ImageGeneratorPlugin,
    PluginBase,
)


class PluginRegistry:
    """插件注册中心。管理四类插件的注册与查找。"""

    def __init__(self) -> None:
        self._ai_models: dict[str, AIModelPlugin] = {}
        self._publishers: dict[str, PublisherPlugin] = {}
        self._formatters: dict[str, FormatterPlugin] = {}
        self._image_generators: dict[str, ImageGeneratorPlugin] = {}

    # -- 注册 --

    def _register(self, store: dict[str, PluginBase], plugin: PluginBase) -> None:
        if plugin.name in store:
            raise ValueError(f"Plugin '{plugin.name}' already registered")
        store[plugin.name] = plugin

    def register_ai_model(self, plugin: AIModelPlugin) -> None:
        self._register(self._ai_models, plugin)

    def register_publisher(self, plugin: PublisherPlugin) -> None:
        self._register(self._publishers, plugin)

    def register_formatter(self, plugin: FormatterPlugin) -> None:
        self._register(self._formatters, plugin)

    def register_image_generator(self, plugin: ImageGeneratorPlugin) -> None:
        self._register(self._image_generators, plugin)

    # -- 查找 --

    def get_ai_model(self, name: str) -> AIModelPlugin | None:
        return self._ai_models.get(name)

    def get_publisher(self, name: str) -> PublisherPlugin | None:
        return self._publishers.get(name)

    def get_formatter(self, name: str) -> FormatterPlugin | None:
        return self._formatters.get(name)

    def get_image_generator(self, name: str) -> ImageGeneratorPlugin | None:
        return self._image_generators.get(name)

    # -- 列表 --

    def list_all(self) -> dict[str, list[str]]:
        return {
            "ai_models": list(self._ai_models.keys()),
            "publishers": list(self._publishers.keys()),
            "formatters": list(self._formatters.keys()),
            "image_generators": list(self._image_generators.keys()),
        }
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_plugin_registry.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add backend/plugins/registry.py tests/test_plugin_registry.py
git commit -m "feat: 插件注册中心 — 注册、查找、列表、去重"
```

---

## Task 7: FastAPI 应用与 API 端点

**Files:**
- Create: `backend/app/main.py`
- Create: `backend/app/api/router.py`
- Create: `backend/app/api/health.py`
- Create: `backend/app/api/plugins.py`
- Create: `tests/conftest.py`
- Create: `tests/test_api_health.py`
- Create: `tests/test_api_plugins.py`

- [ ] **Step 1: 写 API 测试的 conftest**

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.main import create_app


@pytest.fixture
def app(tmp_path):
    """创建测试用 FastAPI 应用"""
    import yaml

    config_file = tmp_path / "config.yaml"
    config_data = {
        "app": {"host": "127.0.0.1", "port": 8000},
    }
    config_file.write_text(yaml.dump(config_data))

    return create_app(config_path=str(config_file), db_path=str(tmp_path / "test.db"))


@pytest.fixture
async def client(app):
    """异步测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
```

- [ ] **Step 2: 写健康检查端点的 failing test**

```python
# tests/test_api_health.py
import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "version" in data


@pytest.mark.asyncio
async def test_root_redirects_or_returns(client):
    resp = await client.get("/")
    assert resp.status_code == 200
```

- [ ] **Step 3: 写插件管理端点的 failing test**

```python
# tests/test_api_plugins.py
import pytest


@pytest.mark.asyncio
async def test_list_plugins_empty(client):
    resp = await client.get("/api/plugins")
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        "ai_models": [],
        "publishers": [],
        "formatters": [],
        "image_generators": [],
    }
```

- [ ] **Step 4: 运行测试确认失败**

Run: `pytest tests/test_api_health.py tests/test_api_plugins.py -v`
Expected: FAIL — `ImportError: cannot import name 'create_app'`

- [ ] **Step 5: 实现健康检查路由**

```python
# backend/app/api/health.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
```

- [ ] **Step 6: 实现插件管理路由**

```python
# backend/app/api/plugins.py
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/plugins")
async def list_plugins(request: Request):
    registry = request.app.state.plugin_registry
    return registry.list_all()
```

- [ ] **Step 7: 实现路由聚合**

```python
# backend/app/api/router.py
from fastapi import APIRouter

from backend.app.api.health import router as health_router
from backend.app.api.plugins import router as plugins_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(plugins_router)
```

- [ ] **Step 8: 实现 FastAPI 应用工厂**

```python
# backend/app/main.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.app.core.config import load_config
from backend.app.core.database import create_engine_from_path, get_session_factory
from backend.app.models.base import Base
from backend.app.api.router import api_router
from backend.plugins.registry import PluginRegistry


def create_app(
    config_path: str = "config.yaml",
    db_path: str = "data/db/app.db",
) -> FastAPI:
    """应用工厂：创建并配置 FastAPI 实例。"""
    config = load_config(config_path)

    app = FastAPI(title="微信公众号自动化系统", version="0.1.0")

    # 数据库
    engine = create_engine_from_path(db_path)
    Base.metadata.create_all(engine)
    app.state.db_session_factory = get_session_factory(engine)

    # 配置
    app.state.config = config

    # 插件注册中心
    app.state.plugin_registry = PluginRegistry()

    # 路由
    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {"message": "微信公众号自动化系统", "version": "0.1.0"}

    return app


# 用于 uvicorn 直接启动: uvicorn backend.app.main:app
app = create_app()
```

- [ ] **Step 9: 运行测试确认通过**

Run: `pytest tests/test_api_health.py tests/test_api_plugins.py -v`
Expected: 3 passed

- [ ] **Step 10: 运行全部测试确认无回归**

Run: `pytest tests/ -v`
Expected: 所有测试通过（约 25 个）

- [ ] **Step 11: Commit**

```bash
git add backend/app/main.py backend/app/api/ tests/conftest.py tests/test_api_health.py tests/test_api_plugins.py
git commit -m "feat: FastAPI 应用工厂 + 健康检查 + 插件列表 API"
```

---

## Task 8: 端到端验证

**Files:** 无新增文件

- [ ] **Step 1: 运行全部测试**

Run: `pytest tests/ -v --tb=short`
Expected: 所有测试通过

- [ ] **Step 2: 手动启动服务验证**

```bash
cd WeChatOfficialAccountAutomationSystem
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

在浏览器或 curl 验证：
- `GET http://127.0.0.1:8000/` → `{"message": "微信公众号自动化系统", "version": "0.1.0"}`
- `GET http://127.0.0.1:8000/api/health` → `{"status": "ok", "version": "0.1.0"}`
- `GET http://127.0.0.1:8000/api/plugins` → `{"ai_models": [], "publishers": [], "formatters": [], "image_generators": []}`

- [ ] **Step 3: 停止服务，推送代码**

```bash
git push origin master
```

---

## Plan 1 完成标准

- [x] FastAPI 服务可启动，3 个端点正常响应
- [x] SQLite 数据库自动创建，5 个数据模型可增删改查
- [x] 插件注册中心支持四类插件的注册、查找、列表
- [x] 配置系统从 YAML 加载，缺省值正确填充
- [x] 所有测试通过
