from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Query

from app.schemas import AuthScheme
from app.managers import TenderManager, get_auth_session


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


@router.post("/goszakup/", tags=["goszakup"])
async def goszakup(
    auth_data: AuthScheme,
    announcement_number: str = Query(default=11257729),
):
    auth_session = await get_auth_session(auth_data)
    tender = TenderManager(auth_session, announcement_number, auth_data)
    await tender.start()
    # try:
    #     auth_session = await get_auth_session(auth_data)
    #     goszakup = TenderManager(auth_session, announcement_number)
    #     await goszakup.goszakup()
    # except RuntimeError as e:
    #     if str(e) == "Session is closed":
    #         auth_session = await get_auth_session(auth_data)
    #         goszakup = TenderManager(auth_session)
    #         await goszakup.goszakup()
