from playwright.async_api import async_playwright, Browser


class PlaywrightDriver:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None

    async def start(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
