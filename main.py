
from fastapi import FastAPI,status, Response, Request,HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from typing import Optional
from router import blog_get, blog_post,users,articles,products,file
from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi.staticfiles import StaticFiles
from templates import templates
import time

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(products.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(templates.router)

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


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["duration"] = str(duration)
    return response


origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.mount("/files",StaticFiles(directory="files"),name="files")
# can access files from browser. http://127.0.0.1:8000/files/pydantic2.png

app.mount("/templates/static",StaticFiles(directory="templates/static"),name="static")