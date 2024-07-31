from fastapi import APIRouter, Query
from app.schemas import AuthScheme
from app.managers import GoszakupAuth, TaxDebtManager

router = APIRouter()


@router.post("/goszakup_auth/", tags=["goszakup"])
async def goszakup_auth(
    auth_data: AuthScheme,
    close_session: bool = False,
):
    auth_manager = GoszakupAuth(auth_data)
    await auth_manager.get_auth_session(head_driver=True)
    if close_session:
        await auth_manager.close_session()
    return {"success": True}


@router.post("/check_tax_debt/", tags=["goszakup"])
async def check_tax_debt(
    auth_data: AuthScheme,
    delta: int = Query(default=10),
):
    tax_debt = TaxDebtManager(auth_data, delta)
    result = await tax_debt.start()
    return result
