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
