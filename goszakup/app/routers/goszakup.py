from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Query

from app.schemas import AuthScheme
from app.managers import GoszakupParser, get_auth_session


router = APIRouter()


@router.post("/auth/", tags=["goszakup"])
async def goszakup_auth(
    auth_data: AuthScheme,
    auth_session: ClientSession = Depends(get_auth_session),
):
    result = {"iin_bin": auth_data.iin_bin, "auth_session_exist": True}
    if not auth_session:
        result["auth_session_exist"] = False
    return result


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
