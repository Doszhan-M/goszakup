import aiohttp
from logging import getLogger
from datetime import datetime, timedelta

from .base import BaseParser
from app.core.config import settings
from app.services import get_aiohttp_session


logger = getLogger("fastapi")
active_sessions = {"aiohttp_session": None}
cookie_time_delta = 110
cookie_time_delta_test = 5


class GoszakupAuthorization(BaseParser):
    """Manager for getting cookie from sud.kz."""

    def __init__(self, aiohttp_session, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self._login_key_url: str = "https://v3bl.goszakup.gov.kz/ru/user/sendkey/kz"

    async def login_goszakup(self) -> any:
        """Log in to sud via eds and return cookie."""

        key_for_sign = await self.async_request("POST", self._login_key_url)
        xml_to_sign = self.build_xml(key_for_sign)
        signed_xml = await self.sign_xml(xml_to_sign, self._eds_auth)
        await self.send_signed_eds(signed_xml)
        await self.send_password()
        self.set_aiohttp_session()
        return self.aiohttp_session

    def set_aiohttp_session(self) -> None:
        active_sessions["aiohttp_session"] = self.aiohttp_session
        active_sessions["set_time"] = datetime.now()
        logger.info("Acquired a new auth cookie!")

    def build_xml(self, key_for_sign) -> str:
        xml = f'<?xml version="1.0" encoding="UTF-8"?><root><key>{key_for_sign}</key></root>'
        return xml

    async def send_signed_eds(self, signed_xml) -> str:
        data = {"sign": signed_xml}
        url = "https://v3bl.goszakup.gov.kz/user/sendsign/kz"
        response_html = await self.async_request("POST", url, payload=data)
        return response_html

    async def send_password(self) -> str:
        data = {"password": settings.GOSZAKUP_PASSWORD, "agreed_check": "on"}
        confirm_url: str = "https://v3bl.goszakup.gov.kz/ru/user/auth_confirm"
        confirm = await self.async_request("POST", confirm_url, payload=data)
        return confirm


async def get_auth_session() -> aiohttp.ClientSession:
    session: aiohttp.ClientSession = active_sessions.get("aiohttp_session")
    if session:
        delta = timedelta(minutes=cookie_time_delta)
        cookie_not_fresh = active_sessions["set_time"] + delta < datetime.now()
        if cookie_not_fresh:
            await session.close()
            session = None
    if not session:
        new_aiohttp_session = await get_aiohttp_session()
        manager = GoszakupAuthorization(new_aiohttp_session)
        session = await manager.login_goszakup()
        print("session: ", session)
    return session
