import secrets

from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

from app.core.config import Settings, get_settings


router = APIRouter()
security = HTTPBasic()


def get_openapi_username(
    settings: Settings = Depends(get_settings),
    credentials: HTTPBasicCredentials = Depends(security),
):
    correct_username = secrets.compare_digest(
        credentials.username,
        settings.OPENAPI_USER,
    )
    correct_password = secrets.compare_digest(
        credentials.password,
        settings.OPENAPI_PASS,
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_openapi_username)):
    return get_swagger_ui_html(openapi_url="openapi.json", title="docs")


@router.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_openapi_username)):
    return get_redoc_html(openapi_url="openapi.json", title="docs")


@router.get("/openapi.json", include_in_schema=False)
async def openapi(request: Request, username: str = Depends(get_openapi_username)):
    app = request.app
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
