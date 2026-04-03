import pytest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from backend.app.models.base import Base
from backend.app.models.style_profile import StyleProfile

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_save_and_load_profile(db_session):
    from backend.app.style_engine.profile import StyleProfileManager
    manager = StyleProfileManager(db_session)
    features = {"vocabulary": {"preferred_words": ["搞定", "踩坑"], "avoided_words": ["赋能"]}, "sentence_patterns": {"avg_length": 18}}
    manager.save(features)
    loaded = manager.get_latest()
    assert loaded is not None
    assert loaded["vocabulary"]["preferred_words"] == ["搞定", "踩坑"]

def test_get_latest_returns_none_when_empty(db_session):
    from backend.app.style_engine.profile import StyleProfileManager
    manager = StyleProfileManager(db_session)
    assert manager.get_latest() is None

def test_save_increments_version(db_session):
    from backend.app.style_engine.profile import StyleProfileManager
    manager = StyleProfileManager(db_session)
    manager.save({"v": 1})
    manager.save({"v": 2})
    profiles = db_session.query(StyleProfile).order_by(StyleProfile.version).all()
    assert len(profiles) == 2
    assert profiles[0].version == 1
    assert profiles[1].version == 2
