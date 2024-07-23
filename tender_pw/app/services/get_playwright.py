from playwright.async_api import async_playwright, Browser, Page
from playwright.async_api._generated import Playwright as AsyncPlaywright

from app.core.config import settings


class PlaywrightDriver:
    def __init__(self):
        self.playwright: AsyncPlaywright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def start(self) -> Page:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=settings.HEADLESS_DRIVER
        )
        self.page = await self.browser.new_page()
        self.page.set_default_timeout(10000)
        return self.page

    async def stop(self) -> None:
        await self.browser.close()
        await self.playwright.stop()
