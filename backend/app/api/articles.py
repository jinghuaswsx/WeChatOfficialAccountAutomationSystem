# backend/app/api/articles.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from backend.app.models.article import Article


class CreateArticleRequest(BaseModel):
    title: str
    key_points: list[str]


class UpdateArticleRequest(BaseModel):
    final_draft: str | None = None
    status: str | None = None


router = APIRouter(prefix="/articles")


@router.get("")
async def list_articles(request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        return [
            {
                "id": a.id,
                "title": a.title,
                "status": a.status,
                "score": a.score,
                "created_at": str(a.created_at) if a.created_at else None,
            }
            for a in articles
        ]


@router.post("")
async def create_article(req: CreateArticleRequest, request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        article = Article(title=req.title, status="extracting")
        db.add(article)
        db.commit()
        db.refresh(article)
        return {
            "id": article.id,
            "title": article.title,
            "status": article.status,
        }


@router.get("/{article_id}")
async def get_article(article_id: int, request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        article = db.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return {
            "id": article.id,
            "title": article.title,
            "status": article.status,
            "outline": article.outline,
            "ai_draft": article.ai_draft,
            "deai_draft": article.deai_draft,
            "final_draft": article.final_draft,
            "score": article.score,
            "score_details": article.score_details,
        }


@router.put("/{article_id}")
async def update_article(article_id: int, req: UpdateArticleRequest, request: Request):
    session_factory = request.app.state.db_session_factory
    with session_factory() as db:
        article = db.get(Article, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        if req.final_draft is not None:
            article.final_draft = req.final_draft
        if req.status is not None:
            article.status = req.status
        db.commit()
        db.refresh(article)
        return {
            "id": article.id,
            "title": article.title,
            "status": article.status,
            "final_draft": article.final_draft,
        }
