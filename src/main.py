from litestar import Litestar, get, Response
from litestar.response import Redirect
from litestar.openapi import OpenAPIConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi import OpenAPIController



class MyOpenAPIController(OpenAPIController):
    path = "/docs"



@get("/")
async def index() -> dict[str, str]:
    return Redirect(path="/docs/swagger")


@get("/status")
async def health() -> dict[str, str]:
    return {"status": "UP"}



@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


app = Litestar(route_handlers=[index, get_book,health],
    openapi_config=OpenAPIConfig(
        title="My API", version="1.0.0", create_examples=True, path="/docs"
    ),
)