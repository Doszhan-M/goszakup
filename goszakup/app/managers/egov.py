from asyncio import sleep
from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from .base import EgovBase
from .cookie_egov import CookieParser
from app.core.config import settings
from app.services import iin_bin_validator, ProjectError


class EgovParser(EgovBase):
    """Manager for parsing to egov."""

    def __init__(self, parturl, iin_bin, session) -> None:
        super().__init__()
        self.parturl: str = parturl
        self.iin_bin: str = iin_bin
        connector = TCPConnector(ssl=False, force_close=True)
        self.session: ClientSession = session
        self.session._connector=connector
        self.cookie_parser = CookieParser()
        self.wait = 5
        self.in_progress_loop_counter = 500

    async def parse(self) -> dict:
        """Start parsing."""

        await self.set_cookie()
        uuid = await self.get_uuid()
        xml = await self.get_xml(uuid)
        signed_xml = await self.sign_xml(xml, self._eds_gos)
        request_number = await self.send_eds(signed_xml, uuid)
        result_urls = await self.waiting_result(request_number)
        return result_urls

    async def set_cookie(self) -> None:
        """Get and set cookie in headers."""

        cookie = await self.cookie_parser.get_or_reload_cookie()
        self.headers["Cookie"] = cookie

    async def get_uuid(self) -> str:
        """Get uuid from signingUrl."""

        if iin_bin_validator.validate_bin(self.iin_bin):
            payload = {"declarantUin": settings.DECLARANTUIN, "bin": self.iin_bin}
        elif iin_bin_validator.validate_iin(self.iin_bin):
            payload = {"declarantUin": settings.DECLARANTUIN, "iin": self.iin_bin}
        url = f"https://egov.kz/services/{self.parturl}/rest/app/get-signing-url"
        self.headers["Referer"] = f"https://egov.kz/services/{self.parturl}/"
        response = await self.post_request(url, payload)
        uuid = response["signingUrl"][-36:]
        self.headers[
            "Referer"
        ] = f"https://egov.kz/services/signing/?PageQueryID={uuid}"
        return uuid

    async def get_xml(self, uuid) -> str:
        """Get xml for sign"""

        url = f"https://egov.kz/services/signing/rest/app/xml?PageQueryID={uuid}"
        response = await self.get_request(url)
        return response["xml"][0]

    async def sign_xml(self, xml, eds) -> str:
        """Sign xml from egov by local ncanode."""

        payload = self.prepare_payload_for_sign(xml, eds)
        self.headers["Content-Type"] = "application/json"
        response = await self.post_request(self._ncanode_url, payload)
        signed_data = self.clear_signed_data(response)
        return signed_data

    async def send_eds(self, signed_xml, uuid) -> str:
        """Sign a request for egov via digital signature."""

        payload = {"xml": [signed_xml], "uuid": uuid, "signingType": "EDS"}
        url = "https://egov.kz/services/signing/rest/app/send-eds"
        self.headers["Content-Type"] = "application/json;charset=UTF-8"
        response = await self.post_request(url, payload)
        return response["requestNumber"]

    async def check_result(self, request_number) -> dict:
        """Get the result of a signed request."""

        url = f"https://egov.kz/services/{self.parturl}/rest/request-states/{request_number}"
        response = await self.get_request(url)
        return response

    async def waiting_result(self, request_number) -> dict:
        """Waiting for result success or failed."""

        in_progress = True
        counter = 0
        while in_progress:
            counter += 1
            await sleep(self.wait)
            self.wait += counter
            result = await self.check_result(request_number)
            approved = result["status"] == "APPROVED"
            rejected = result["status"] == "REJECTED"
            declined = result["status"] == "DECLINED"
            if approved or rejected or declined:
                in_progress = False
            if counter > self.in_progress_loop_counter:
                raise ProjectError("endless loop in_progress")
        if approved:
            result_urls = {"ru": "", "kz": ""}
            links = result["resultsForDownload"]
            # print('links: ', links)
            if not links:
                return result["statusGo"]
            for link in links:
                if link["language"] == "ru":
                    result_urls["ru"] = link["url"]
                elif link["language"] == "kz":
                    result_urls["kz"] = link["url"]
        else:
            result_urls = result
        return result_urls
