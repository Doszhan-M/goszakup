from playwright.async_api import async_playwright, Browser, Page


class PlaywrightDriver:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.page: Page = None

    async def start(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.route(
                "**/*",
                lambda route: (
                    route.abort()
                    if route.request.resource_type in ["stylesheet", "image"]
                    else route.continue_()
                ),
            )
            return self.page
            
    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
