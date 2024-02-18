from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Query

from app.schemas import AuthScheme
from app.managers import TenderManager, get_auth_session


router = APIRouter()


@router.post("/goszakup_auth/", tags=["goszakup"])
def goszakup_auth(
    auth_data: AuthScheme,
    auth_session: ClientSession = Depends(get_auth_session),
):
    result = {"iin_bin": auth_data.iin_bin, "auth_session_exist": True}
    if not auth_session:
        result["auth_session_exist"] = False
    return result


@router.post("/tender_check/", tags=["goszakup"])
def tender_check(
    auth_data: AuthScheme,
    announce_number: str = Query(default=11656750),
):
    auth_session = get_auth_session(auth_data)
    with TenderManager(auth_session, announce_number, auth_data) as tender:
        result = tender.check_announce()
    return result


@router.post("/tender_start/", tags=["goszakup"])
def tender_start(
    auth_data: AuthScheme,
    announce_number: str = Query(default=11608669),
):
    auth_session = get_auth_session(auth_data)
    with TenderManager(auth_session, announce_number, auth_data) as tender:
        result = tender.start()
    return result
