from uuid import uuid4
from time import sleep
from logging import getLogger
from playwright.async_api import Page

from app.services import PlaywrightDriver


logger = getLogger("fastapi")
active_sessions = {}


class GoszakupAuth:
    """Manager for getting cookie from goszakup.gov.kz."""

    def __init__(self, auth_data, *args, **kwargs):
        self.auth_url = "https://v3bl.goszakup.gov.kz/ru/user/"
        self.zero_page = "https://v3bl.goszakup.gov.kz/ru/insurance"
        self.goszakup_pass = auth_data.goszakup_pass
        self.ssid = uuid4()
        self.playwright_manager = PlaywrightDriver()
        self.page: Page = None
        self.auth_data = auth_data

    async def get_auth_session(self):
        await self.playwright_manager.start()
        self.page = await self.playwright_manager.browser.new_page()
        await self.page.goto(self.auth_url)
        nclayer_call_btn = await self.page.query_selector("#selectP12File")
        print('nclayer_call_btn: ', nclayer_call_btn)
        # if self.eds_manager.is_not_busy():
        #     await nclayer_call_btn.click()
        #     await self.eds_manager.execute_sign_by_eds("auth_eds")
        #     await self.page.wait_for_timeout(1000)
        # await self.enter_goszakup_password()
        await self.store_auth_session()
        return self.page

    async def enter_goszakup_password(self):
        password_field = await self.page.query_selector("input[name='password']")
        await password_field.fill(self.goszakup_pass)
        checkbox = await self.page.query_selector("#agreed_check")
        if not await checkbox.is_checked():
            await checkbox.click()
        login_button = await self.page.query_selector(".btn-success")
        await login_button.click()

    async def store_auth_session(self):
        global active_sessions
        active_sessions[self.ssid] = {"page": self.page}
        logger.info(f"Store new session id: {self.ssid}")

    async def close_session(self):
        if self.ssid in active_sessions:
            session = active_sessions[self.ssid]
            await session["page"].close()
            del active_sessions[self.ssid]
            logger.info(f"Closed and removed session id: {self.ssid}")
