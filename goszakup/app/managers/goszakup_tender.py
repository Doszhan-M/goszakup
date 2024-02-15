import asyncio
from logging import getLogger

from .base import BaseParser
from app.core.config import settings


logger = getLogger("fastapi")


class GoszakupParser(BaseParser):
    
    def __init__(self, aiohttp_session, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self.url: str = "https://v3bl.goszakup.gov.kz/ru/announce/index/11257729"

    async def goszakup(self) -> any:

        async with self.aiohttp_session.get(self.url) as response:
            response_text = await response.text()
            with open("app/test.html", "w") as file:
                file.write(response_text)
        return response_text
