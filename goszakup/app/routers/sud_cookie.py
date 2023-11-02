from aiohttp import ClientSession
from fastapi import APIRouter, Depends

from app.managers import SudCookieParser
from app.services import tenacity_retry, get_aiohttp_session


router = APIRouter()


@router.get("/sud/cookie/reload", tags=["sud"])
@tenacity_retry
async def reload_cookie(
    aiohttp_session: ClientSession = Depends(get_aiohttp_session),
):
    """Reload sud cookie."""

    manager = SudCookieParser(aiohttp_session)
    cookie = await manager.reload_cookie()
    return cookie


@router.get("/sud/cookie/get", tags=["sud"])
async def get_cookie():
    """Get saved sud cookie."""

    cookie = await SudCookieParser.get_cookie()
    return cookie


@router.get("/get_or_reload", tags=["sud"])
@tenacity_retry
async def get_or_reload_cookie(
    aiohttp_session: ClientSession = Depends(get_aiohttp_session),
):
    """Get cookie or reload if it is not or expire."""

    manager = SudCookieParser(aiohttp_session)
    cookie = await manager.get_or_reload_cookie()
    return cookie
