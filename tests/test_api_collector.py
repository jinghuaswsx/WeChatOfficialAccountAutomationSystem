import pytest

@pytest.mark.asyncio
async def test_scan_sessions_endpoint(client):
    resp = await client.get("/api/collector/scan")
    assert resp.status_code == 200
    data = resp.json()
    assert "sessions" in data
    assert "publishable" in data

@pytest.mark.asyncio
async def test_list_key_points_empty(client):
    resp = await client.get("/api/collector/key-points")
    assert resp.status_code == 200
    assert resp.json() == []
