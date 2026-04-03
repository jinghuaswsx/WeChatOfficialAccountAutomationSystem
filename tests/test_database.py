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
