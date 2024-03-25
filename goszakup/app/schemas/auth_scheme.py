from pydantic import BaseModel

from app.core.config import settings


class AuthScheme(BaseModel):
    eds_auth: str = (
        settings.BASE_DIR
        + "/static/eds/AUTH_RSA256_bc70569f74c3201c5d019b787895f44979d30440.p12"
    )
    eds_gos: str = (
        settings.BASE_DIR
        + "/static/eds/GOSTKNCA_a3623558da98644ba2a46a5dc4bc177181236eee.p12"
    )
    eds_pass: str = "Aa1234"
    goszakup_pass: str = "87014333488Aa"



