from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Query

from app.managers import get_goszakup_auth_session, GoszakupParser


router = APIRouter()


@router.get("/auth/", tags=["goszakup"])
async def auth_goszakup(
    goszakup_auth_session: ClientSession = Depends(get_goszakup_auth_session),
):
    if goszakup_auth_session:
        return {"success": True}
    return {"success": False}


@router.get("/goszakup/", tags=["goszakup"])
async def goszakup(
    announcement_number: str = Query(default=555555),
    goszakup_auth_session: ClientSession = Depends(get_goszakup_auth_session),
):
    try:
        goszakup = GoszakupParser(goszakup_auth_session)
        await goszakup.goszakup()
    except RuntimeError as e:
        if str(e) == "Session is closed":
            goszakup_auth_session = await get_goszakup_auth_session()
            goszakup = GoszakupParser(goszakup_auth_session)
            await goszakup.goszakup()
