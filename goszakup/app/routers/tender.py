from fastapi import APIRouter, Query

from app.schemas import AuthScheme
from app.managers import TenderManager


router = APIRouter()


@router.post("/tender_check/", tags=["goszakup"])
def tender_check(
    auth_data: AuthScheme,
    announce_number: str = Query(default=11656750),
):
    tender = TenderManager(announce_number, auth_data)
    result = tender.check_announce()
    return result


@router.post("/tender_start/", tags=["goszakup"])
def tender_start(
    auth_data: AuthScheme,
    announce_number: str = Query(default=11674559),
):

    tender = TenderManager(announce_number, auth_data)
    result = tender.start()
    return result
