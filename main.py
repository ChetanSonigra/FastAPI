
from fastapi import FastAPI,status, Response, Request,HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from enum import Enum
from typing import Optional
from router import blog_get, blog_post,users,articles
from db import models
from db.database import engine
from exceptions import StoryException

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(users.router)
app.include_router(articles.router)


@app.get('/hello')             # get = operation, ('/') = endpoint
def index():                   # operation function
    return {'message': 'Hello World!'}



@app.post('/hello')
def index2():
    return 'HI'


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418,
                        content=exc.name)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(status_code=400,
                             content=str(exc))

models.Base.metadata.create_all(engine)

