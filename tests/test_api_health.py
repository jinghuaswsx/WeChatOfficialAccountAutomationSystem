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
async def test_root_without_static_returns_404(client):
    """Without static files, root returns 404 (static mount not active)."""
    resp = await client.get("/")
    assert resp.status_code == 404
