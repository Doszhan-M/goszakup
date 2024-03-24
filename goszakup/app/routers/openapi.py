from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi import Request
from fastapi.security import HTTPBasic
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


router = APIRouter()
security = HTTPBasic()


@router.get("/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="openapi.json", title="docs")


@router.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(openapi_url="openapi.json", title="docs")


@router.get("/openapi.json", include_in_schema=False)
async def openapi(request: Request):
    app = request.app
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
