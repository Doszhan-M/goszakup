from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException


class ProjectError(Exception):
    pass


class SignatureFound(Exception):
    """Exception raised when a signature is found in the document table."""

    pass


class TenderStartFailed(HTTPException):
    def __init__(self, announce_number) -> None:
        status_code = 500
        error_code = "tender_not_start"
        detail = {
            "error_code": error_code,
            "description": f"Тендер №{announce_number} не начался на сайте! Количество попыток исчерпано!",
        }
        super().__init__(status_code, detail)
