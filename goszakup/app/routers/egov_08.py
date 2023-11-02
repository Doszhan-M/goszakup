from aiohttp import ClientSession
from fastapi import APIRouter, Query, Depends

from app.managers import EgovParser
from app.services import tenacity_retry, get_aiohttp_session
from app.scrapers import E080Scraper, E083Scraper


router = APIRouter()


@router.get("/e080", tags=["egov"])
@tenacity_retry
async def e080(
    iin_bin: str = Query(default="071140021902", min_length=12, max_length=12),
    session: ClientSession = Depends(get_aiohttp_session),
):
    """Предоставление сведений о всех регистрационных действиях юридического лица."""

    parser = EgovParser("P30.05", iin_bin, session)
    urls = await parser.parse()
    scraper = E080Scraper(urls, session, parser.headers, iin_bin)
    result = await scraper.scraping_pages()
    return result


@router.get("/e083", tags=["egov"])
@tenacity_retry
async def e083(
    iin_bin: str = Query(default="170540000477", min_length=12, max_length=12),
    session: ClientSession = Depends(get_aiohttp_session),
):
    """Предоставление сведений о наложенных обременениях (арест) на
    долю юридического лиц."""

    parser = EgovParser("P30.08", iin_bin, session)
    urls = await parser.parse()
    scraper = E083Scraper(urls, session, parser.headers, iin_bin)
    result = await scraper.scraping_pages()
    return result
