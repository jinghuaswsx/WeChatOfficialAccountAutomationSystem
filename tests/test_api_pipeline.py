import pytest

@pytest.mark.asyncio
async def test_pipeline_status_idle(client):
    resp = await client.get("/api/pipeline/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "idle"
