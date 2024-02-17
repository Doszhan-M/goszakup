from pydantic import BaseModel


class AuthScheme(BaseModel):
    iin_bin: str = "141140001428"
    eds_auth: str = "/home/asus/github/goszakup/eds/AUTH_RSA256_bc70569f74c3201c5d019b787895f44979d30440.p12"
    eds_gos: str = "/home/asus/github/goszakup/eds/GOSTKNCA_a3623558da98644ba2a46a5dc4bc177181236eee.p12"
    eds_pass: str = "Aa1234"
    goszakup_pass: str = "ZAQwsxcde32"
