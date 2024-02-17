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
        self.application_url = (
            f"https://v3bl.goszakup.gov.kz/ru/application/create/{announce_number}"
        )
        self.application_create = f"https://v3bl.goszakup.gov.kz/ru/application/ajax_create_application/{announce_number}"
        self.all_applications = "https://v3bl.goszakup.gov.kz/ru/myapp"

    async def start(self) -> any:
        await self.waiting_until_the_start()
        application_data = await self.collect_application_data()
        success = await self.request_application(application_data)
        if success:
            docs_url = await self.get_docs_url()
            required_docs_urls = await self.get_required_docs_links(docs_url)
            res = await self.sign_docs(required_docs_urls)
        # docs_url = await self.get_docs_url()
        # required_docs_urls = await self.get_required_docs_links(docs_url)
        # res = await self.sign_docs(required_docs_urls)

    async def sign_docs(self, required_docs_urls) -> any:
        """Подписать документы."""

        for link in required_docs_urls:
            print('link: ', link)
            data = {"generate": "Y"}
            generate = await self.async_request("POST", link, payload=data)
            soup = BeautifulSoup(generate, "html.parser")
            signature_block = soup.find_all("div", class_="add_signature_block")
            print('signature_block: ', signature_block)



    async def get_required_docs_links(self, docs_url) -> list:
        """Вернуть список ссылок на документы обязательных для подписания."""

        all_docs = await self.async_request("GET", docs_url)
        soup = BeautifulSoup(all_docs, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        required_docs = []
        for row in rows:
            if "Не Обязателен" not in row.text:
                link = row.find("a", href=True)
                if link:
                    required_docs.append(link["href"])
        return required_docs

    async def get_docs_url(self) -> str:
        """После создания заявки надо получить url для подписания документов."""

        all_applications = await self.async_request("GET", self.all_applications)
        soup = BeautifulSoup(all_applications, "html.parser")
        links = soup.find_all(
            "a",
            href=lambda href: href and self.announce_number in href,
            class_="btn btn-default",
        )
        link = links[0]["href"]
        url = "https://v3bl.goszakup.gov.kz" + link
        return url

    async def request_application(self, application_data) -> bool:
        """Отправить запрос на создание заявки."""

        create_response = await self.async_request(
            "POST", self.application_create, payload=application_data, decode="json"
        )
        if create_response["status"] == "ok":
            return True
        return False

    async def collect_application_data(self) -> dict:
        """Запросить страницу заявки и собрать данные для подачи заявки."""

        application_response = await self.async_request(
            "GET", self.application_url, decode=None
        )
        while application_response.status == 404:
            await asyncio.sleep(1)
            application_response = await self.async_request(
                "GET", self.application_url, decode=None
            )
        if application_response.status == 200:
            raw_data = await application_response.text()
            application_data = self.gather_application_data(raw_data)
            return application_data

    def gather_application_data(self, raw_data) -> dict:
        """Собрать необходимый данные для подачи заявки."""

        soup = BeautifulSoup(raw_data, "html.parser")
        address_option = soup.find("select", {"name": "subject_address"}).find(
            lambda option: "050061" in option.text if option else False
        )
        address = address_option["value"].replace(" ", "+") if address_option else None
        iik_option = soup.find("select", {"name": "iik"}).find(
            lambda option: ("KZ5696502F0017154550" in option.text if option else False)
        )
        iik = iik_option["value"].replace(" ", "+") if iik_option else None
        phone_option = soup.find("select", {"name": "contact_phone"}).find(
            lambda option: "7014333488" in option.text if option else False
        )
        phone = (
            phone_option["value"].strip().replace(" ", "+") if phone_option else None
        )
        data = {"subject_address": address, "iik": iik, "contact_phone": phone}
        return data

    async def waiting_until_the_start(self) -> None:
        """Ждать до времени старта указанной в карте."""

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
        logger.info(f"Start tender {datetime.now()}")

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
