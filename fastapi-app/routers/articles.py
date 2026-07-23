"""
文章相关路由 —— 全部以 /articles 开头
"""
from fastapi import APIRouter

router = APIRouter(prefix="/articles", tags=["文章管理"])


@router.get("/")
async def list_articles():
    """实际访问路径：/articles/"""
    return {"msg": "文章列表"}


@router.get("/{article_id}")
async def get_article(article_id: int):
    """实际访问路径：/articles/5"""
    return {"msg": f"文章详情", "article_id": article_id}
