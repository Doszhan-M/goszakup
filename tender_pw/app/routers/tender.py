import time

from fastapi import APIRouter, Query

from app.schemas import TenderScheme
from app.managers import TenderManager, TenderCancelManager


router = APIRouter()


@router.post("/tender_check/", tags=["tender"])
async def tender_check(
    auth_data: TenderScheme,
    announce_number: str = Query(default=11695620),
):
    start_time = time.time()
    tender = TenderManager(announce_number, auth_data)
    result = await tender.check_announce()
    process_time = time.time() - start_time
    print(f"Tender check processed in {process_time:.4f} seconds")
    return result


@router.post("/tender_start/", tags=["tender"])
async def tender_start(
    auth_data: TenderScheme,
    announce_number: str = Query(default=12728973),
):

    tender = TenderManager(announce_number, auth_data)
    # result = await tender.start()
    result = await tender.start_with_retry()
    return result


@router.post("/tender_cancel/", tags=["tender"])
async def tender_cancel(
    auth_data: TenderScheme,
    announce_number: str = Query(default=12736661),
):
    cancel_manager = TenderCancelManager(announce_number, auth_data)
    result = await cancel_manager.cancel()
    await cancel_manager.close_session()
    return result
