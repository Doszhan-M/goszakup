from fastapi import APIRouter, Query
from app.schemas import AuthScheme
from app.managers import GoszakupAuth

router = APIRouter()


@router.post("/goszakup_auth/", tags=["goszakup"])
async def goszakup_auth(
    auth_data: AuthScheme,
    close_session: bool = True,
):
    auth_manager = GoszakupAuth(auth_data)
    await auth_manager.get_auth_session()
    if close_session:
        await auth_manager.close_session()
    return {"success": True}
