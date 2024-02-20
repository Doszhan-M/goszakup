from fastapi import APIRouter

from app.schemas import AuthScheme
from app.managers import GoszakupAuthorization


router = APIRouter()


@router.post("/goszakup_auth/", tags=["goszakup"])
def goszakup_auth(
    auth_data: AuthScheme,
    close_session: bool = False,
):
    auth_manager = GoszakupAuthorization(auth_data)
    auth_manager.get_auth_session()
    if close_session:
        auth_manager.close_session()
    return {"success": True}
