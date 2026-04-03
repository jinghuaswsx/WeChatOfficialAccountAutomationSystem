import pytest

@pytest.mark.asyncio
async def test_get_style_profile_empty(client):
    resp = await client.get("/api/style/profile")
    assert resp.status_code == 200
    assert resp.json()["profile"] is None

@pytest.mark.asyncio
async def test_upload_samples(client):
    resp = await client.post("/api/style/samples", json={"samples": ["今天搞了一天代码。", "这个功能折腾了半天。"]})
    assert resp.status_code == 200
    assert resp.json()["status"] == "accepted"
