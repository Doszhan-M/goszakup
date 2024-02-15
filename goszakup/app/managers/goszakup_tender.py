from logging import getLogger
from bs4 import BeautifulSoup

from .base import BaseParser


logger = getLogger("fastapi")


class TenderManager(BaseParser):

    def __init__(self, aiohttp_session, announce_number, auth_data, *args, **kwargs):
        super().__init__(aiohttp_session=aiohttp_session, *args, **kwargs)
        self.eds_gos: str = auth_data.eds_gos
        self.eds_pass: str = auth_data.eds_pass
        self.announce_url: str = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )

    async def check_announce(self) -> dict:
        result = {"success": True}
        response_text = await self.async_request("GET", self.announce_url)
        announce_detail = self.gather_announce_data(response_text)
        result.update(announce_detail)
        return result

    def gather_announce_data(self, raw_data):
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
