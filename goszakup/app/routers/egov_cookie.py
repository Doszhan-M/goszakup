from fastapi import APIRouter

from app.managers import CookieParser
from app.services import tenacity_retry


router = APIRouter()


@router.get("/reload", tags=["cookie"])
async def reload_cookie():
    """Reload_cookie."""

    manager = CookieParser()
    cookie = await manager.reload_cookie()
    return cookie


@router.get("/get", tags=["cookie"])
async def get_cookie():
    """Get saved cookie."""

    cookie = await CookieParser.get_cookie()
    return cookie


@router.get("/get_or_reload", tags=["cookie"])
@tenacity_retry
async def get_or_reload_cookie():
    """Get cookie or reload if it is not or expire."""

    manager = CookieParser()
    cookie = await manager.get_or_reload_cookie()
    return cookie
