import aiohttp
from typing import AsyncIterator


async def get_aiohttp_session() -> AsyncIterator[aiohttp.ClientSession]:
    try:
        async with aiohttp.ClientSession() as session:
            yield session
    finally:
        await session.close()


class AiohttpSession:
    def __init__(self):
        self.session = None

    async def start(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
            return self.session

    async def stop(self):
        if self.session:
            await self.session.close()
