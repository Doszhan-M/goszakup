from fastapi import HTTPException


class ProjectError(Exception):
    pass


class RequestFailed(HTTPException):
    def __init__(self, status_code, url, html) -> None:
        error_code = "request_failed"
        if status_code == 500:
            error_code = "goszakup_server_error"
        detail = {
            "error_code": error_code,
            "url": url,
            "response_status_code": status_code,
            "HTML": html,
        }
        super().__init__(status_code, detail)


class TenderStartFailed(HTTPException):
    def __init__(self, announce_number) -> None:
        status_code = 200
        error_code = "tender_not_start"
        detail = {
            "success": False,
            "error_code": error_code,
            "description": f"Тендер №{announce_number} не начался на сайте! Количество попыток исчерпано!",
        }
        super().__init__(status_code, detail)
