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
