from fastapi import APIRouter, Query

from app.schemas import AuthScheme
from app.managers import GoszakupAuthorization, TaxDebtManager


router = APIRouter()


@router.post("/goszakup_auth/", tags=["goszakup"])
def goszakup_auth(
    auth_data: AuthScheme,
    close_session: bool = True,
):
    auth_manager = GoszakupAuthorization(auth_data)
    auth_manager.get_auth_session()
    if close_session:
        auth_manager.close_session()
    return {"success": True}


@router.post("/check_tax_debt/", tags=["goszakup"])
def check_tax_debt(
    auth_data: AuthScheme,
    delta: int = Query(default=10),
):

    tax_debt = TaxDebtManager(auth_data, delta)
    result = tax_debt.start()
    return result
