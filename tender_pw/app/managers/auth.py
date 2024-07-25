import grpc
from uuid import uuid4
from logging import getLogger
from playwright.async_api import Page

from app.pb2 import eds_pb2
from app.pb2 import eds_pb2_grpc
from app.services import PlaywrightDriver
from playwright._impl._errors import TimeoutError
from app.core.config import settings


logger = getLogger("fastapi")
active_sessions = {}


class GoszakupAuth:
    """Manager for getting cookie from goszakup.gov.kz."""

    auth_url = "https://v3bl.goszakup.gov.kz/ru/user/"

    def __init__(self, auth_data, *args, **kwargs):
        self.playwright_manager = PlaywrightDriver()
        self.page: Page = None
        self.auth_data = auth_data
        self.ssid = uuid4()
        self.wake_up_screen()

    async def get_auth_session(self) -> Page:
        try:
            self.page = await self.playwright_manager.start()
            await self.page.goto(self.auth_url, wait_until="domcontentloaded")
            nclayer_call_btn = await self.page.query_selector("#selectP12File")
            async with grpc.aio.insecure_channel(settings.SIGNER_HOST) as channel:
                stub = eds_pb2_grpc.EdsServiceStub(channel)
                eds_manager_status = stub.SendStatus(eds_pb2.EdsManagerStatusCheck())
                async for status in eds_manager_status:
                    if status.busy.value:
                        logger.info("Eds Service is busy. Waiting...")
                await nclayer_call_btn.click()
                eds_data = eds_pb2.SignByEdsStart(
                    eds_path=self.auth_data.eds_gos,
                    eds_pass=self.auth_data.eds_pass,
                )
                sign_by_eds = await stub.ExecuteSignByEds(eds_data)
                if sign_by_eds.result:
                    await self.enter_goszakup_password()
            await self.store_auth_session()
            return self.page
        except Exception:
            await self.playwright_manager.stop()
            logger.error("Error while get_auth_session")
            raise

    async def enter_goszakup_password(self):
        password_field = await self.page.wait_for_selector("input[name='password']")
        await password_field.fill(self.auth_data.goszakup_pass)
        checkbox = await self.page.query_selector("#agreed_check")
        await checkbox.click()
        login_button = await self.page.query_selector(".btn-success")
        try:
            await login_button.click(timeout=1000)
        except TimeoutError:
            pass

    async def store_auth_session(self):
        global active_sessions
        active_sessions[self.ssid] = {"page": self.page}
        logger.info(f"Store new session id: {self.ssid}")

    async def close_session(self):
        if self.ssid in active_sessions:
            del active_sessions[self.ssid]
            await self.playwright_manager.stop()
            logger.info(f"Closed and removed session id: {self.ssid}")


