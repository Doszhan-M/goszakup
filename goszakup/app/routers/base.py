from fastapi import APIRouter

from . import openapi
from . import goszakup
from . import tender

router = APIRouter()


router.include_router(openapi.router, prefix="/goszakup")
router.include_router(goszakup.router, prefix="/goszakup")
router.include_router(tender.router, prefix="/goszakup")
