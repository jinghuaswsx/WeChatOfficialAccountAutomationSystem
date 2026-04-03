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
