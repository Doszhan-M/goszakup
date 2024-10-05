from pydantic import BaseModel

from app.core.config import settings


class AuthScheme(BaseModel):
    eds_gos: str = (
        settings.BASE_DIR
        + "/static/eds/GOST512_b79a7a0994373be5fb329692fd8f5774cddb6af8.p12"
    )
    eds_pass: str = "Aa1234"
    goszakup_pass: str = "87014333488Aa@"
