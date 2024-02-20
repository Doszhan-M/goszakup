from time import sleep
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .eds import EdsManager
from app.services.exception import TenderStartFailed


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
        application_page = self.tender_start()
        self.fill_application_data(application_page)
        sleep(50)
        # success = await self.request_application(application_data)
        # if success:
        #     docs_url = await self.get_docs_url()
        #     required_docs_urls = await self.get_required_docs_links(docs_url)
        #     res = await self.sign_docs(required_docs_urls)

    def fill_application_data(self, soup: BeautifulSoup) -> any:
        """Заполнить необходимы поля заявки."""

        must_select_data = {
            "subject_address": "050061",
            "iik": "KZ5696502F0017154550",
            "contact_phone": "7014333488",
        }
        for field_name, partial_value in must_select_data.items():
            print(field_name)
            select_element = self.web_driver.find_element(By.NAME, field_name)
            print("select_element: ", select_element)
            select = Select(select_element)
            for option in select.options:
                if partial_value in option.get_attribute("value"):
                    select.select_by_value(option.get_attribute("value"))
                    break
        # address_option = soup.find("select", {"name": "subject_address"}).find(
        #     lambda option: "050061" in option.text if option else False
        # )
        # address = address_option["value"].replace(" ", "+") if address_option else None
        # iik_option = soup.find("select", {"name": "iik"}).find(
        #     lambda option: ("KZ5696502F0017154550" in option.text if option else False)
        # )
        # iik = iik_option["value"].replace(" ", "+") if iik_option else None
        # phone_option = soup.find("select", {"name": "contact_phone"}).find(
        #     lambda option: "7014333488" in option.text if option else False
        # )
        # phone = (
        #     phone_option["value"].strip().replace(" ", "+") if phone_option else None
        # )
        # data = {"subject_address": address, "iik": iik, "contact_phone": phone}
        # return data

    def tender_start(self, try_count=2):
        """Запросить страницу заявки и ждать фактическое начало тендера."""

        self.web_driver.get(self.application_url)
        application = self.web_driver.page_source
        soup = BeautifulSoup(application, "html.parser")
        elements = soup.find_all(class_="content-block")
        tender_not_starting = any(
            "Страница не найдена" in element.text for element in elements
        )
        if try_count == 0:
            raise TenderStartFailed(self.announce_number)
        elif tender_not_starting:
            sleep(1)
            try_count -= 1
            return self.tender_start(try_count)

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
