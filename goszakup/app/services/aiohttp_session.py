import aiohttp


async def get_new_aiohttp_session() -> aiohttp.ClientSession:
    async with aiohttp.ClientSession() as session:
        return session
