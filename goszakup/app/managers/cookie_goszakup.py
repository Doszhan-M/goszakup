import ssl
from logging import getLogger
from aiohttp import TCPConnector
from aiohttp.cookiejar import CookieJar

from app.services import aioredis
from app.core.config import settings
from .base import EgovBase, BaseParser


logger = getLogger("fastapi")


class GoszakupCookieParser(BaseParser, EgovBase):
    """Manager for getting cookie from sud.kz."""

    def __init__(self, aiohttp_session, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = TCPConnector(ssl=ssl_context)
        self.aiohttp_session._connector = connector
        self._login_key_url: str = "https://v3bl.goszakup.gov.kz/ru/user/sendkey/kz"
        self._confirm_url: str = "https://v3bl.goszakup.gov.kz/ru/user/auth_confirm"

    async def login_goszakup(self) -> CookieJar:
        """Log in to sud via eds and return cookie."""

        key_for_sign = await self.async_request("POST", self._login_key_url)
        xml_to_sign = self.build_xml(key_for_sign)
        signed_xml = await self.sign_xml(xml_to_sign, self._eds_auth)
        await self.send_signed_eds(signed_xml)
        await self.send_password()
        url = "https://v3bl.goszakup.gov.kz/ru/cabinet/profile"
        response= await self.async_request("GET", url, decode=None)
        response_cookies = response.cookies
        print('response_cookies: ', response_cookies)

        raw_cookie = self.aiohttp_session.cookie_jar
        cookies = self.bake_cookie(raw_cookie)
        return cookies

    async def send_password(self) -> str:
        data = {"password": settings.GOSZAKUP_PASSWORD, "agreed_check": "on"}
        confirm = await self.async_request("POST", self._confirm_url, payload=data)
        return confirm

    def build_xml(self, key_for_sign) -> str:
        xml = f'<?xml version="1.0" encoding="UTF-8"?><root><key>{key_for_sign}</key></root>'
        return xml

    async def sign_xml(self, xml, eds) -> str:
        """Sign xml from egov by local ncanode"""

        payload = self.prepare_payload_for_sign(xml, eds)
        headers = {"Content-Type": "application/json"}
        signed_xml = await self.async_request(
            "POST",
            self._ncanode_url,
            headers=headers,
            payload=payload,
            decode="json",
        )
        signed_data = self.clear_signed_data(signed_xml)
        return signed_data

    async def send_signed_eds(self, signed_xml) -> str:
        data = {"sign": signed_xml}
        url = "https://v3bl.goszakup.gov.kz/user/sendsign/kz"
        response_html = await self.async_request("POST", url, payload=data)
        return response_html

    def bake_cookie(self, raw_cookie: CookieJar) -> str:
        """Get session cookie."""

        cookies = raw_cookie.filter_cookies("https://v3bl.goszakup.gov.kz")
        session_cookie = cookies.get("ci_session").value
        return session_cookie
