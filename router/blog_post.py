from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(prefix='/blog',
                   tags=['blog'])

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tag: list[str]=[]
    metadata: Dict[str,str]={'k1': 'v1'}
    image: Optional[Image]= None

@router.post('/new/{id}')
def create_blog(blog: BlogModel,id: int, version: int = 1):
    return {
            'id': id,
            'data': blog,
            'version': version
            }

@router.post('/new/{id}/comment/{comment_id}')
def create_comment(blog: BlogModel, id: int, 
                   comment_title: str = Query(None,
                                           title='Title of the comment',
                                            description='Some description of comment title',
                                            alias='commentTitle',
                                            deprecated=True),
                   content: str = Body(Ellipsis,
                                       min_length=10,
                                       max_length=50,
                                       regex='^[a-z\s]*$'),
                   comment_id: int = Path(gt=5, lt=10),
                   v: Optional[list[str]] = Query(['1.0','1.1','1.2'])
    ):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'comment_id': comment_id,
        'content': content
    }
