import aiohttp
from logging import getLogger
from datetime import datetime, timedelta

from fastapi import Depends

from .base import BaseParser
from app.schemas import AuthScheme
from app.services import get_aiohttp_session, active_sessions


logger = getLogger("fastapi")


class GoszakupAuthorization(BaseParser):
    """Manager for getting cookie from sud.kz."""

    def __init__(self, aiohttp_session, auth_data, *args, **kwargs):
        super().__init__(aiohttp_session, *args, **kwargs)
        self._login_key_url: str = "https://v3bl.goszakup.gov.kz/ru/user/sendkey/kz"
        self.iin_bin: str = auth_data.iin_bin
        self.eds_auth: str = auth_data.eds_auth
        self.eds_pass: str = auth_data.eds_pass
        self.goszakup_pass: str = auth_data.goszakup_pass
        self.session_expire = 60  # minute

    async def login_goszakup(self) -> any:
        """Log in to sud via eds and return cookie."""

        key_for_sign = await self.async_request("POST", self._login_key_url)
        xml_to_sign = self.build_xml(key_for_sign)
        signed_xml = await self.sign_xml(xml_to_sign, self.eds_auth, self.eds_pass)
        await self.send_signed_eds(signed_xml)
        await self.send_password()
        await self.store_aiohttp_session()
        return self.aiohttp_session

    def build_xml(self, key_for_sign) -> str:
        xml = f'<?xml version="1.0" encoding="UTF-8"?><root><key>{key_for_sign}</key></root>'
        return xml

    async def send_signed_eds(self, signed_xml) -> str:
        data = {"sign": signed_xml}
        url = "https://v3bl.goszakup.gov.kz/user/sendsign/kz"
        response_html = await self.async_request("POST", url, payload=data)
        return response_html

    async def send_password(self) -> str:
        data = {"password": self.goszakup_pass, "agreed_check": "on"}
        confirm_url: str = "https://v3bl.goszakup.gov.kz/ru/user/auth_confirm"
        confirm = await self.async_request("POST", confirm_url, payload=data)
        return confirm

    async def store_aiohttp_session(self) -> None:
        delta = timedelta(minutes=self.session_expire)
        session = {"session": self.aiohttp_session, "expire": datetime.now() + delta}
        active_sessions[self.iin_bin] = session
        logger.info(f"Store new session for {self.iin_bin}!")


async def get_auth_session(auth_data: AuthScheme = Depends()) -> aiohttp.ClientSession:
    auth_session = active_sessions.get(auth_data.iin_bin)
    if auth_session:
        session: aiohttp.ClientSession = auth_session["session"]
        if auth_session["expire"] < datetime.now():
            await session.close()
            auth_session = None
    if not auth_session:
        new_aiohttp_session = await get_aiohttp_session()
        manager = GoszakupAuthorization(new_aiohttp_session, auth_data)
        session = await manager.login_goszakup()
    return session
