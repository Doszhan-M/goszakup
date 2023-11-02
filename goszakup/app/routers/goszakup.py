from aiohttp import ClientSession
from fastapi import APIRouter, Depends

from app.managers import GoszakupCookieParser
from app.services import tenacity_retry, get_aiohttp_session


router = APIRouter()


@router.get("/goszakup/cookie/reload", tags=["goszakup"])
async def reload_cookie(
    aiohttp_session: ClientSession = Depends(get_aiohttp_session),
):
    """Reload sud cookie."""

    manager = GoszakupCookieParser(aiohttp_session)
    cookie = await manager.login_goszakup()
    return cookie
