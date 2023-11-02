import re
import json
from json import dumps
from requests import request
from logging import getLogger
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError

from app.core.config import settings
from app.services.exception import ProjectError, AsyncRequestFailed


logger = getLogger("fastapi")


class EgovBase:
    """Main class with common parameters for descendants"""

    _cookie_key: str = "egov_cookie"
    _cookie_ttl: int = 900
    _login_url: str = "https://idp.egov.kz/idp/login?lvl=2&url=https%3A%2F%2Fegov.kz%2Fcms%2Fcallback%2Fauth%2Fcms%2F"
    _eds_auth: str = settings.EDSAUTH
    _eds_gos: str = settings.EDSGOS
    _eds_pass: str = settings.EDSPASS
    _ncanode_url: str = settings.NCANODEURL
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/json;charset=UTF-8",
        "Connection": "keep-alive",
        "Origin": "https://egov.kz",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "document",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Referer": "",
        "Cookie": "",
    }

    async def post_request(self, url, payload) -> dict:
        """Send post request by aiohttp."""

        data = dumps(payload)
        async with self.session.post(url, headers=self.headers, data=data) as response:
            try:
                result = await response.json()
                return result
            except ContentTypeError:
                logger.error(
                    f"status-{response.status},\n headers-{self.headers},\n text-{await response.text()}",
                )
                raise ProjectError(f"Error when post_request {await response.text()}")

    def sync_post_request(self, url, payload) -> dict:
        """Send post request by requests."""

        response = request(
            "POST",
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        return response.json()

    async def get_request(self, url) -> dict:
        """Send get request by aiohttp."""

        async with self.session.get(url, headers=self.headers) as response:
            result = await response.json()
            return result

    def prepare_payload_for_sign(self, xml, eds) -> dict:
        """Prepare payload for sign by ncanode."""

        xml = re.sub("<\?xml[^>]+>", "", xml)
        payload = {
            "version": "1.0",
            "method": "XML.sign",
            "params": {
                "checkCrl": "false",
                "checkOcsp": "false",
                "p12": eds,
                "password": self._eds_pass,
                "xml": xml,
                "createTsp": False,
                "verifyOcsp": "false",
                "verifyCrl": "false",
                "useTsaPolicy": "TSA_GOST_POLICY",
            },
        }
        return payload

    def clear_signed_data(self, signed_xml) -> str:
        """Get the required key."""

        signed_data = str(signed_xml["result"]["xml"])
        return signed_data


class BaseParser:
    """Common methods to parsers."""

    def __init__(self, aiohttp_session, *args, **kwargs) -> None:
        self.aiohttp_session: ClientSession = aiohttp_session


    async def async_request(
        self,
        method,
        url,
        headers={"content-type": "application/x-www-form-urlencoded"},
        payload=None,
        decode="text",
    ) -> str | dict:
        """Send request by aiohttp."""

        if (
            isinstance(payload, dict)
            and headers.get("Content-Type") == "application/json"
        ):
            payload = dumps(payload).encode("utf-8")
        async with self.aiohttp_session.request(
            method, url, headers=headers, data=payload
        ) as response:
            if response.status not in (200,):
                html = await response.text()
                raise AsyncRequestFailed(response.status, url, html)
            if decode == "text":
                return await response.text()
            elif decode == "json":
                return await response.json()
            elif not decode:
                return response
