from time import sleep
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By

from .eds import EdsManager


logger = getLogger("fastapi")


class TenderManager(EdsManager):

    def __init__(
        self, auth_session, announce_number, auth_data, *args, **kwargs
    ) -> None:
        super().__init__(auth_data=auth_data, session=auth_session, *args, **kwargs)
        self.announce_number = announce_number
        self.announce_url: str = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )
        self.application_url = (
            f"https://v3bl.goszakup.gov.kz/ru/application/create/{announce_number}"
        )

    def start(self) -> any:
        self.waiting_until_the_start()
        application_data = self.tender_start()
        # success = await self.request_application(application_data)
        # if success:
        #     docs_url = await self.get_docs_url()
        #     required_docs_urls = await self.get_required_docs_links(docs_url)
        #     res = await self.sign_docs(required_docs_urls)

    def tender_start(self) -> BeautifulSoup:
        """Запросить страницу заявки и ждать фактическое начало тендера."""

        self.web_driver.get(self.application_url)
        application = self.web_driver.page_source
        soup = BeautifulSoup(application, "html.parser")
        elements = soup.find_all(class_="content-block")
        tender_not_starting = any(
            "Страница не найдена" in element.text for element in elements
        )
        while tender_not_starting:
            sleep(1)
            print("Tender not start!")
            return self.tender_start()
        return soup

    def waiting_until_the_start(self) -> None:
        """Ждать до времени старта указанной в карте."""

        self.web_driver.get(self.announce_url)
        announce = self.web_driver.page_source
        announce_detail = self.gather_announce_data(announce)
        announce_detail["start_time"] = "2024-02-18 13:29:00"
        start_time_format = "%Y-%m-%d %H:%M:%S"
        start_time = datetime.strptime(announce_detail["start_time"], start_time_format)
        now = datetime.now()
        if start_time > now:
            wait_seconds = (start_time - now).total_seconds()
            logger.info(f"Waiting {wait_seconds} seconds for {self.announce_number}.")
            sleep(wait_seconds)
        logger.info(f"Starting tender at {datetime.now()} for {self.announce_number}")

    def check_announce(self) -> any:
        result = {"success": True}
        self.web_driver.get(self.announce_url)
        announce = self.web_driver.page_source
        announce_detail = self.gather_announce_data(announce)
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
