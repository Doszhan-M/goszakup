import re
import ssl
from json import dumps
from logging import getLogger
from aiohttp import TCPConnector
from aiohttp import ClientSession

from app.core.config import settings
from app.services.exception import RequestFailed


logger = getLogger("fastapi")


class BaseParser:
    """Common methods to parsers."""

    def __init__(self, aiohttp_session, *args, **kwargs) -> None:
        self.aiohttp_session: ClientSession = aiohttp_session
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = TCPConnector(ssl=ssl_context)
        self.aiohttp_session._connector = connector

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
                raise RequestFailed(response.status, url, html)
            if decode == "text":
                return await response.text()
            elif decode == "json":
                return await response.json()
            elif not decode:
                return response

    def prepare_payload_for_sign(self, xml, eds, eds_pass) -> dict:
        """Prepare payload for sign by ncanode."""

        xml = re.sub(r"<\?xml[^>]+>", "", xml)
        payload = {
            "version": "1.0",
            "method": "XML.sign",
            "params": {
                "checkCrl": "false",
                "checkOcsp": "false",
                "p12": eds,
                "password": eds_pass,
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

    async def sign_xml(self, xml, eds, eds_pass) -> str:
        """Sign xml from egov by local ncanode"""

        payload = self.prepare_payload_for_sign(xml, eds, eds_pass)
        headers = {"Content-Type": "application/json"}
        signed_xml = await self.async_request(
            "POST",
            settings.NCANODEURL,
            headers=headers,
            payload=payload,
            decode="json",
        )
        signed_data = self.clear_signed_data(signed_xml)
        return signed_data
