from aiohttp import ClientSession
from fastapi import APIRouter, Query, Depends

from app.managers import EgovParser
from app.services import tenacity_retry, get_aiohttp_session
from app.scrapers import E032Scraper, E034Scraper, E035Scraper


router = APIRouter()


@router.get("/e032", tags=["egov"])
@tenacity_retry
async def e032(
    iin_bin: str = Query(default="941240000193", min_length=12, max_length=12),
    session: ClientSession = Depends(get_aiohttp_session),
):
    """Предоставление сведений о зарегистрированном юридическом лице,
    филиале или представительстве, учредители other_heads
    """

    parser = EgovParser("P30.01", iin_bin, session)
    urls = await parser.parse()
    scraper = E032Scraper(urls, session, parser.headers, iin_bin)
    result = await scraper.scraping_pages()
    return result


@router.get("/e034", tags=["egov"])
@tenacity_retry
async def e034(
    iin_bin: str = Query(default="941240000193", min_length=12, max_length=12),
    session: ClientSession = Depends(get_aiohttp_session),
):
    """Предоставление сведений об участии юридического лица
    в других юридических лицах
    """

    parser = EgovParser("P30.03", iin_bin, session)
    urls = await parser.parse()
    scraper = E034Scraper(urls, session, parser.headers, iin_bin)
    result = await scraper.scraping_pages()
    return result


@router.get("/e035", tags=["egov"])
@tenacity_retry
async def e035(
    iin_bin: str = Query(default="630607401888", min_length=12, max_length=12),
    session: ClientSession = Depends(get_aiohttp_session),
):
    """Предоставление сведений об участии физического лица в
    юридических лицах, филиалах и представительствах
    """

    parser = EgovParser("P30.04", iin_bin, session)
    urls = await parser.parse()
    scraper = E035Scraper(urls, session, parser.headers, iin_bin)
    result = await scraper.scraping_pages()
    return result
