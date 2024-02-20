from time import sleep
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

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

    def start(self) -> dict:
        self.waiting_until_the_start()
        self.tender_start()
        # self.fill_and_submit_application()
        # required_docs_urls = self.get_required_docs_links()
        # for url in required_docs_urls:
        #     self.generate_document(url)
        #     self.sign_document()
        # self.next_page()
        self.web_driver.get("https://v3bl.goszakup.gov.kz/ru/application/preview/11674559/53090028")
        self.apply_application()
        result = self.check_application_result()
        sleep(50)
        return result

    def check_application_result(self) -> dict:
        "После подтверждения может выйти ошибка."
        
        result = {"success": True, "error_text" : None, "success_text" : None}
        try:
            success = WebDriverWait(self.web_driver, 30).until(
                EC.element_to_be_clickable((By.ID, "success"))
            )
            result["success_text"] = success.text
        except TimeoutException:
            error = WebDriverWait(self.web_driver, 30).until(
                EC.element_to_be_clickable((By.ID, "errors"))
            )
            result["success"] = False
            result["error_text"] = error.text
        return result
        
    def apply_application(self) -> None:
        "Нажать кнопку подать заявку."

        apply_button = WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='next' and contains(text(), 'Подать заявку')]")
            )
        )
        apply_button.click()
        yes_button = WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.ID, "btn_price_agree"))
        )
        yes_button.click()

    def next_page(self) -> None:
        "Вернуться к списку документов и нажать далее."

        while True:
            try:
                footer = WebDriverWait(self.web_driver, 30).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "panel-footer"))
                )
                button = footer.find_element(By.TAG_NAME, "a")
                button.click()
                break
            except StaleElementReferenceException:
                pass
        next_button = WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.ID, "next"))
        )
        next_button.click()

    def sign_document(self) -> None:
        "Подписать документ ЭЦП."

        call_bnt = self.web_driver.find_element(By.CSS_SELECTOR, ".btn-add-signature")
        self.execute_sign_by_eds("gos_eds", call_bnt)

    def generate_document(self, url) -> None:
        "Сформировать документ."

        self.web_driver.get(url)
        submit_button = self.web_driver.find_element(By.CSS_SELECTOR, ".btn.btn-info")
        submit_button.click()

    def get_required_docs_links(self) -> list:
        """Вернуть список ссылок на документы обязательных для подписания."""

        WebDriverWait(self.web_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "docs"))
        )
        html = self.web_driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        required_docs = []
        for row in rows:
            if "Не Обязателен" not in row.text:
                link = row.find("a", href=True)
                if link:
                    required_docs.append(link["href"])
        return required_docs

    def fill_and_submit_application(self) -> None:
        """Заполнить необходимые поля заявки и подать заявку."""

        must_select_data = {
            "subject_address": "050061",
            "iik": "KZ5696502F0017154550",
            "contact_phone": "7014333488",
        }
        for field_name, search_text in must_select_data.items():
            select_element = self.web_driver.find_element(By.NAME, field_name)
            select = Select(select_element)
            for option in select.options:
                if search_text in option.text:
                    select.select_by_visible_text(option.text)
                    break
        next_button = self.web_driver.find_element(By.ID, "next-without-captcha")
        next_button.click()

    def tender_start(self, try_count=3600) -> None:
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
