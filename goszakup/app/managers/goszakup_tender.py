import asyncio
from logging import getLogger

from .base import BaseParser


logger = getLogger("fastapi")


class TenderManager(BaseParser):

    def __init__(self, aiohttp_session, announcement_number, auth_data, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self.eds_gos: str = auth_data.eds_gos
        self.eds_pass: str = auth_data.eds_pass        
        self.url: str = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announcement_number}"
        )

    async def start(self) -> any:

        async with self.aiohttp_session.get(self.url) as response:
            response_text = await response.text()
            with open("app/test.html", "w") as file:
                file.write(response_text)
        return response_text
