from fastapi import APIRouter
from fastapi.responses import Response, PlainTextResponse, HTMLResponse

router = APIRouter(prefix="/products",
                   tags=["products"])

product_list = ["watch","camera","phone"]

@router.get("/all")
def get_all_products():
    data = " ".join(product_list)
    return Response(content=data, media_type="text/plain")

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