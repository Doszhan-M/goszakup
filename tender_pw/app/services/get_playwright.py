import os
import asyncio
from playwright.async_api import async_playwright, Browser, Page
from playwright.async_api._generated import Playwright as AsyncPlaywright

from app.core.config import settings


class PlaywrightDriver:
    def __init__(self):
        self.playwright: AsyncPlaywright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def start(self, head_driver=None) -> Page:
        self.playwright = await async_playwright().start()
        if head_driver:
            self.browser = await self.playwright.chromium.launch(headless=False)
        else:
            self.browser = await self.playwright.chromium.launch(
                headless=settings.HEADLESS_DRIVER
            )
        self.page = await self.browser.new_page()
        self.page.set_default_timeout(5000)
        await self.wake_up_screen()
        return self.page

    async def stop(self) -> None:
        await self.browser.close()
        await self.playwright.stop()

    @staticmethod
    async def wake_up_screen():
        """Необходимо чтобы при выполнении операций, экран был включен.
        Если экран погас из-за бездействия, можно включить его эмуляцией движения мышки.
        """
        await asyncio.to_thread(os.system, "xdotool mousemove 70 70")
