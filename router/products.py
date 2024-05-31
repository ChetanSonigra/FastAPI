from fastapi import APIRouter, Header, Cookie,Form
from fastapi.responses import Response, PlainTextResponse, HTMLResponse
from typing import List, Optional
from custom_log import log

router = APIRouter(prefix="/products",
                   tags=["products"])

product_list = ["watch","camera","phone"]


@router.post("/new")
def create_product(name: str = Form(...)):
    product_list.append(name)
    return product_list

@router.get("/all")
def get_all_products():
    log("MyAPI", "Call to get all products")
    data = " ".join(product_list)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie("test_cookie","test_cookie_value")
    return response

@router.get("/withheaders")
def get_products(
    response: Response,
    custom_header: Optional[List[str]] = Header(["A","b"]),
    test_cookie: Optional[str] = Cookie(None)
):
    response.headers["custom_response_headers"] = " and ".join(custom_header)
    return {
        "data": product_list,
        "custom-headers": custom_header,
        "cookies": test_cookie
        }

@router.get("/{id}",responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
            }
        },
        "dependencies": "Returns html of an object."
    },
    404: {
        "content": {
            "text/plain": {
                "example": "Product not available"
            }
        },
        "dependencies": "A cleartext error message"
    }
})
def get_product(id:int):
    if id >= len(product_list):
        out = "Product not available"
        return PlainTextResponse(status_code=404,content=out, media_type="text/plain")
    product = product_list[id]
    out = f"""
            <head>
                <style>
                .product {{
                    width: 500px;
                    height: 30px;
                    border: 2px inset green;
                    background-color: lightblue;
                    text-align: center;
                }}
                </style>
                <div class="product">{product}</div>
            </head>
        """
    
    return HTMLResponse(content=out, media_type="text/html")