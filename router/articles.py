from fastapi import APIRouter, Depends
from schemas import ArticleDisplay, ArticleBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_article
from auth.oauth2 import oauth2schema, get_current_user
from schemas import UserBase, UserDisplay, User


router = APIRouter(prefix='/article',tags=['article'])

@router.post('/',response_model=ArticleDisplay)
def create_article(request: ArticleBase,db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return db_article.creatr_article(db,request)


@router.get('/{id}')#,response_model=ArticleDisplay)
def get_article(id: int, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    return {
        "data": db_article.get_article(db,id),
        "current_user": User.model_validate(current_user)
    }

