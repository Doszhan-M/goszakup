from fastapi import APIRouter

from . import openapi
from . import goszakup

router = APIRouter()


router.include_router(openapi.router, prefix="/goszakup")
router.include_router(goszakup.router, prefix="/goszakup")
