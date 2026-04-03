import pytest

@pytest.mark.asyncio
async def test_score_text_endpoint(client):
    resp = await client.post("/api/scorer/score", json={"text": "今天搞了一天代码，挺有意思的。"})
    assert resp.status_code == 200
    data = resp.json()
    assert "total_score" in data
    assert "passed" in data
    assert "dimensions" in data
