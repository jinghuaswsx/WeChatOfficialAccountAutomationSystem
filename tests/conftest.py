# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.main import create_app


@pytest.fixture
def app(tmp_path):
    import yaml
    config_file = tmp_path / "config.yaml"
    config_data = {"app": {"host": "127.0.0.1", "port": 8000}}
    config_file.write_text(yaml.dump(config_data))
    return create_app(config_path=str(config_file), db_path=str(tmp_path / "test.db"))


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
