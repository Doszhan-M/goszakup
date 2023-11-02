from asyncio import sleep
from bs4 import BeautifulSoup
from logging import getLogger
from aiohttp.cookiejar import CookieJar

from app.services import aioredis
from .base import EgovBase, BaseParser


logger = getLogger("fastapi")


class SudCookieParser(BaseParser, EgovBase):
    """Manager for getting cookie from sud.kz."""

    _updating_key = "sud_cookie_updating"
    _cookie_ttl = 6600  # 110 min
    _cookie_key: str = "sud_cookie"

    def __init__(self, aiohttp_session, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self._login_url: str = "https://office.sud.kz/loginByEDS.xhtml"

    async def get_or_reload_cookie(self) -> str:
        """Get cookie or reload if it is not or expire."""

        cookie = await self.get_cookie()
        if not cookie:
            cookie = await self.reload_cookie()
        return cookie

    @classmethod
    async def get_cookie(cls) -> str:
        """Get cookie from redis."""

        cookie: bytes = await aioredis.get(cls._cookie_key)
        if cookie:
            return cookie.decode("utf-8")

    async def reload_cookie(self) -> str:
        """Login sud.kz, get and save cookie to redis"""

        updating = await aioredis.get(self._updating_key)
        if not updating:
            raw_cookie = await self.login_sud()
            cookie = self.bake_cookie(raw_cookie)
            await aioredis.set(self._cookie_key, cookie, self._cookie_ttl)
            await aioredis.delete(self._updating_key)
            return cookie
        while updating:
            logger.info("sud cookies updating")
            await sleep(5)
            updating = await aioredis.get(self._updating_key)
        cookie = await self.get_cookie()
        return cookie

    async def login_sud(self) -> CookieJar:
        """Log in to sud via eds and return cookie."""

        response_html = await self.async_request("GET", self._login_url)
        soup = BeautifulSoup(response_html, "lxml")
        view_state = soup.find(id="javax.faces.ViewState")["value"]
        xml_to_sign = soup.find(id="xmlToSign0")["value"]
        signed_xml = await self.sign_xml(xml_to_sign, self._eds_auth)
        await self.send_signed_eds(signed_xml, view_state)
        raw_cookie = self.aiohttp_session.cookie_jar
        return raw_cookie

    async def send_signed_eds(self, signed_data, view_state) -> str:
        data = {
            "j_idt34": "j_idt34",
            "j_idt34:signedXml": signed_data,
            "j_idt34:j_idt42": "",
            "javax.faces.ViewState": view_state,
            "javax.faces.source": "j_idt34:j_idt52",
            "javax.faces.partial.execute": "j_idt34:j_idt52 @component",
            "javax.faces.partial.render": "@component",
            "org.richfaces.ajax.component": "j_idt34:j_idt52",
            "j_idt34:j_idt52": "j_idt34:j_idt52",
            "rfExt": "null",
            "AJAX:EVENTS_COUNT": "1",
            "javax.faces.partial.ajax": "true",
        }
        url = "https://office.sud.kz/loginByEDS.xhtml"
        response_html = await self.async_request("POST", url, payload=data)
        return response_html

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

    def bake_cookie(self, raw_cookie: CookieJar) -> str:
        """Get session cookie."""

        cookies = raw_cookie.filter_cookies("https://office.sud.kz")
        session_cookie = cookies.get("JSESSIONID").value
        return session_cookie
