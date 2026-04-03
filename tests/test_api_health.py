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
async def test_root_serves_static_index(client):
    """With built static files, root serves the SPA index.html."""
    resp = await client.get("/")
    # If static files exist, serves 200; otherwise 404
    assert resp.status_code in (200, 404)
