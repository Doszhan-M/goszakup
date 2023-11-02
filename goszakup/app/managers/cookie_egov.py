import asyncio
import aiohttp
from logging import getLogger

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from .base import EgovBase
from app.services import get_web_driver
from app.services import aioredis, redis


logger = getLogger("fastapi")


class CookieParser(EgovBase):
    """Manager for getting cookie from egov."""

    async def reload_cookie(self) -> str:
        """Login egov, get cookie, save cookie to redis"""

        updating = await aioredis.get("updating")
        if not updating:
            await aioredis.delete(self._cookie_key)
            await aioredis.set("updating", "True", 300)
            raw_cookie = await asyncio.to_thread(self.login_egov)
            cookie = self.bake_cookie(raw_cookie)
            await self.cookie_set_to_redis(cookie)
            await aioredis.delete("updating")
            return cookie
        while updating:
            logger.info("cookies_updating")
            await asyncio.sleep(5)
            updating = await aioredis.get("updating")
        cookie = await self.get_cookie()
        return cookie

    @classmethod
    async def get_cookie(cls) -> str:
        """Get cookie from redis."""

        cookie: bytes = await aioredis.get(cls._cookie_key)
        if cookie:
            return cookie.decode("utf-8")

    @classmethod
    def get_cookie_sync(cls) -> str:
        """Get cookie from redis sync."""

        cookie: str = redis.get(cls._cookie_key)
        if cookie:
            return cookie

    async def get_or_reload_cookie(self) -> str:
        """Get cookie or reload if it is not or expire."""

        spent_time = await self.cookie_spent_time()
        cookie = await self.get_cookie()
        if (
            spent_time == 0
            or spent_time
            and spent_time <= self._cookie_ttl - 120
            and cookie
            and len(cookie) > 200
        ):
            cookie = await self.get_cookie()
        else:
            cookie = await self.check_cookie_relevance()
            if not cookie:
                await self.reload_cookie()
                return await self.get_or_reload_cookie()
        return cookie

    def login_egov(self) -> list:
        """Log in to egov via eds and return cookie."""

        web_driver = get_web_driver()
        driver: Chrome = next(web_driver)
        driver.get(self._login_url)
        driver.find_element(By.ID, "certificate-nav-tab").click()
        xml_to_sign = driver.find_element(By.ID, "xmlToSign").get_attribute("value")
        cleaned_xml_to_sign = xml_to_sign.replace('"', '\\"')
        signed_data = self.sign_xml(cleaned_xml_to_sign, self._eds_auth)
        hidden_field = driver.find_element(By.ID, "certificate")
        driver.execute_script(
            "arguments[0].setAttribute('value', arguments[1])",
            hidden_field,
            signed_data,
        )
        driver.find_element(By.ID, "eds_form").submit()
        raw_cookie = driver.get_cookies()
        return raw_cookie

    def sign_xml(self, xml, eds) -> str:
        """Sign xml from egov by local ncanode"""

        payload = self.prepare_payload_for_sign(xml, eds)
        response = self.sync_post_request(self._ncanode_url, payload)
        signed_data = self.clear_signed_data(response)
        return signed_data

    def bake_cookie(self, raw_cookie) -> str:
        """Cookie as a string."""

        cookie = ""
        for i in raw_cookie:
            name = i["name"]
            value = i["value"]
            cookie += f"{name}={value};"
        cookie = cookie[:-1]
        return cookie

    async def cookie_set_to_redis(self, cookie) -> None:
        """Save egov cookie in redis store."""

        await aioredis.set(self._cookie_key, cookie, self._cookie_ttl)

    @classmethod
    async def cookie_spent_time(cls) -> int:
        """Retrieve the elapsed time of a cookie since it was saved."""

        seconds = await aioredis.ttl(cls._cookie_key)
        if seconds != -2:
            spent_time = cls._cookie_ttl - seconds
            return spent_time

    async def check_cookie_relevance(self) -> str:
        """Send a request to user_info to check if the cookie is
        up to date."""

        cookie = await self.get_cookie()
        if cookie:
            url = "https://egov.kz/cms/auth/user.json"
            headers = {
                "authority": "egov.kz",
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "cookie": cookie,
                "referer": "https://egov.kz/cms/kk",
                "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        user_iin = result["user_iin"]
                        if user_iin and len(user_iin) == 12:
                            await self.cookie_set_to_redis(cookie)
                            return cookie
                    logger.info("cookie is expired")
