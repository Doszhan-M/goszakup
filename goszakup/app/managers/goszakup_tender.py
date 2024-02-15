import asyncio
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime

from .base import BaseParser


logger = getLogger("fastapi")


class TenderManager(BaseParser):

    def __init__(self, aiohttp_session, announce_number, auth_data, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self.eds_gos: str = auth_data.eds_gos
        self.eds_pass: str = auth_data.eds_pass
        self.announce_number = announce_number
        self.announce_url: str = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )

    async def start(self) -> any:
        announce = await self.async_request("GET", self.announce_url)
        announce_detail = self.gather_announce_data(announce)
        # announce_detail["start_time"] = "2024-02-15 22:29:00"
        start_time_format = "%Y-%m-%d %H:%M:%S"
        start_time = datetime.strptime(announce_detail["start_time"], start_time_format)
        now = datetime.now()
        if start_time > now:
            wait_seconds = (start_time - now).total_seconds()
            logger.info(f"Waiting for {wait_seconds} seconds.")
            await asyncio.sleep(wait_seconds)
        logger.info(f"continue {datetime.now()}")
        crate_url = (
            f"https://v3bl.goszakup.gov.kz/ru/application/create/{self.announce_number}"
        )
        for i in range(0, 100):
            announce_create = await self.async_request("GET", crate_url)
            path = f"app/services/tmp/test{i}.html"
            self.save_to_file(announce_create, path)
            await asyncio.sleep(10)

    async def check_announce(self) -> dict:
        result = {"success": True}
        response_text = await self.async_request("GET", self.announce_url)
        announce_detail = self.gather_announce_data(response_text)
        result.update(announce_detail)
        return result

    def gather_announce_data(self, raw_data) -> dict:
        announce_detail = {}
        targets_and_label_texts = [
            ("announce_name", "Наименование объявления"),
            ("announce_status", "Статус объявления"),
            ("start_time", "Срок начала приема заявок"),
            ("finish_time", "Срок окончания приема заявок"),
        ]
        soup = BeautifulSoup(raw_data, "html.parser")
        labels = soup.find_all("label")
        for label in labels:
            for key, label_text in targets_and_label_texts:
                if label_text in label.text:
                    next_input = label.find_next("input")
                    input_value = next_input.get("value")
                    announce_detail[key] = input_value
        return announce_detail

    def save_to_file(self, text, path="app/test.html") -> None:
        with open(path, "w") as file:
            file.write(text)
