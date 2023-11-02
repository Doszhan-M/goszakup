from fastapi import APIRouter

from . import egov_08
from . import egov_03
from . import egov_cookie
from . import openapi
from . import sud_cookie
from . import goszakup

router = APIRouter()


router.include_router(openapi.router, prefix="/egov")
router.include_router(goszakup.router, prefix="/egov/parser")
router.include_router(egov_cookie.router, prefix="/egov/cookie")
router.include_router(egov_03.router, prefix="/egov/parser")
router.include_router(egov_08.router, prefix="/egov/parser")
router.include_router(sud_cookie.router, prefix="/egov/parser")
