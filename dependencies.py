from fastapi import APIRouter, Request, Depends
from custom_log import log


router = APIRouter(prefix="/dependencies",
                   tags=["dependencies"],
                   dependencies=[Depends(log)])  # global dependencies

def convert_query_params(request: Request, separator: str):
    out_query = []
    for key,value in request.query_params.items():
        out_query.append(f"{key} {separator} {value}")
    return out_query

def convert_headers(request: Request,separator: str="--",query = Depends(convert_query_params)):  # multilevel dependencies.
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f"{key} {separator} {value}")
    return {
        "query": query,
        "headers": out_headers
    }

@router.get("")
def get_headers(headers = Depends(convert_headers)):
    return {
        "items": ["a","b","c"],
        "headers": headers
    }

@router.post("/new")
def create_item(headers = Depends(convert_headers)):
    return {
        "result": "New item created",
        "headers": headers
    }


# Class Dependency:

class Account:
    def __init__(self,name:str, email:str) -> None:
        self.name = name
        self.email = email

@router.post("/user")
def create_user(name: str, email: str, password: str, account: Account= Depends(Account)): # you can just do Depends() if type is defined.
    return {
        "name": account.name,
        "email": account.email,
    }
    

# Multi level Dependencies:
