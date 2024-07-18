import time

from fastapi import APIRouter, Query

from app.schemas import TenderScheme
from app.managers import TenderManager, TenderCancelManager


router = APIRouter()


@router.post("/tender_check/", tags=["tender"])
def tender_check(
    auth_data: TenderScheme,
    announce_number: str = Query(default=11695620),
):
    start_time = time.time()
    tender = TenderManager(announce_number, auth_data)
    result = tender.check_announce()
    process_time = time.time() - start_time
    print(f"Tender check processed in {process_time:.4f} seconds")
    return {"result": result, "process_time": process_time}


@router.post("/tender_start/", tags=["tender"])
def tender_start(
    auth_data: TenderScheme,
    announce_number: str = Query(default=11695620),
):

    tender = TenderManager(announce_number, auth_data)
    result = tender.start_with_retry()
    return result


@router.post("/tender_cancel/", tags=["tender"])
def tender_start(
    auth_data: TenderScheme,
    announce_number: str = Query(default=11695620),
):

    tender = TenderCancelManager(announce_number, auth_data)
    result = tender.cancel()
    tender.close_session()
    return result
