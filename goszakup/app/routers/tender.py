from fastapi import APIRouter, Query

from app.schemas import TenderScheme
from app.managers import TenderManager


router = APIRouter()


@router.post("/tender_check/", tags=["tender"])
def tender_check(
    auth_data: TenderScheme,
    announce_number: str = Query(default=11729838),
):
    tender = TenderManager(announce_number, auth_data)
    result = tender.check_announce()
    return result


@router.post("/tender_start/", tags=["tender"])
def tender_start(
    auth_data: TenderScheme,
    announce_number: str = Query(default=11688546),
):

    tender = TenderManager(announce_number, auth_data)
    result = tender.start()
    return result
