from fastapi import APIRouter, FastAPI, status, Response
from enum import Enum
from typing import Optional

router = APIRouter(prefix='/blog',tags=['blog'])

@router.get('/all',tags=['blog'],
         summary='Retrieve all blogs', 
         description='This API call simulates fetching all blogs.',
         response_description='List of available blogs')
def get_all_blogs(page=1,pagesize: Optional[int]=None):
    return {"message": f"All {pagesize} blogs on page {page}"}
# order of endpoints is important.


@router.get('/{id}/comment/{comment_id}', tags=['blog','comment'])
def get_comment(id: int, comment_id: int, valid: bool=True, username: Optional[str]=None):
    """
    Simulates retrieving a comment of a blog

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** Boolean query parameter - Defaults to True
    - **username** Optional query parameter
    """
    return {'message': f"id: {id}, comment: {comment_id}, valid: {valid}, username: {username}"}

# Predefined path with Enum:
class Blogtype(str,Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{type}',tags=['blog'])
def get_blog_type(type: Blogtype):
    return {"Blog type": f"{type}"}


@router.get('/{id}',status_code=status.HTTP_200_OK,tags=['blog'])         # Path parameters
def get_blog(id: int,response: Response):
    if id>5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Blog {id} not found!"
    return f"This is blog {id}"
