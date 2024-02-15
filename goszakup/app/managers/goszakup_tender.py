import asyncio
from logging import getLogger

from .base import BaseParser


logger = getLogger("fastapi")


class TenderManager(BaseParser):

    def __init__(self, aiohttp_session, announce_number, auth_data, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self.eds_gos: str = auth_data.eds_gos
        self.eds_pass: str = auth_data.eds_pass
        self.announce_url: str = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )

    async def start(self) -> any:
        pass

    def save_to_file(self, text, path="app/test.html") -> None:
        with open(path, "w") as file:
            file.write(text)
