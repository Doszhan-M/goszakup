import aiohttp


async def get_aiohttp_session() -> aiohttp.ClientSession:
    try:
        async with aiohttp.ClientSession() as session:
            yield session
    finally:
        await session.close()
