
from fastapi import FastAPI,status, Response
from enum import Enum
from typing import Optional
from router import blog_get, blog_post

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get('/hello')             # get = operation, ('/') = endpoint
def index():                   # operation function
    return {'message': 'Hello World!'}



@app.post('/hello')
def index2():
    return 'HI'


