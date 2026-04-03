# tests/test_api_articles.py
import pytest


@pytest.mark.asyncio
async def test_list_articles_empty(client):
    resp = await client.get("/api/articles")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_article(client):
    resp = await client.post("/api/articles", json={
        "title": "测试文章",
        "key_points": ["搭建了项目骨架"],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "测试文章"
    assert data["status"] == "extracting"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_article(client):
    create_resp = await client.post("/api/articles", json={
        "title": "另一篇",
        "key_points": ["实现了插件系统"],
    })
    article_id = create_resp.json()["id"]

    resp = await client.get(f"/api/articles/{article_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "另一篇"


@pytest.mark.asyncio
async def test_update_article_draft(client):
    create_resp = await client.post("/api/articles", json={
        "title": "待编辑",
        "key_points": ["测试"],
    })
    article_id = create_resp.json()["id"]

    resp = await client.put(f"/api/articles/{article_id}", json={
        "final_draft": "这是我修改后的终稿内容。",
    })
    assert resp.status_code == 200
    assert resp.json()["final_draft"] == "这是我修改后的终稿内容。"
