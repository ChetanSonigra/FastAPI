from .models import DbArticle
from schemas import ArticleBase, ArticleDisplay
from sqlalchemy.orm.session import Session


def creatr_article(db: Session, request: ArticleBase):
    new_article = DbArticle(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id = request.user_id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_article(db: Session, id: int):
    return db.query(DbArticle).filter(DbArticle.id == id).first()
