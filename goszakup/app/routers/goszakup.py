from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Query

from app.managers import get_auth_session, GoszakupParser


router = APIRouter()


@router.get("/auth/", tags=["goszakup"])
async def goszakup_auth(
    auth_session: ClientSession = Depends(get_auth_session),
):
    if auth_session:
        return {"success": True}
    return {"success": False}


@router.get("/goszakup/", tags=["goszakup"])
async def goszakup(
    announcement_number: str = Query(default=555555),
    auth_session: ClientSession = Depends(get_auth_session),
):
    try:
        goszakup = GoszakupParser(auth_session)
        await goszakup.goszakup()
    except RuntimeError as e:
        if str(e) == "Session is closed":
            auth_session = await get_auth_session()
            goszakup = GoszakupParser(auth_session)
            await goszakup.goszakup()
