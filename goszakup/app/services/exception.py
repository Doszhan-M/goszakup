from fastapi import HTTPException


class ProjectError(Exception):
    pass


class AsyncRequestFailed(HTTPException):
    def __init__(self, status_code, url, html) -> None:
        detail = {
            "error_code": "AsyncRequestFailed",
            "url": url,
            "status_code": status_code,
            "HTML": html,
        }
        super().__init__(status_code, detail)
