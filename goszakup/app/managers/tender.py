from time import sleep
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from .eds import EdsManager
from app.services import WebDriverManager
from .auth import GoszakupAuthorization
from app.services.exception import TenderStartFailed


logger = getLogger("fastapi")
business_logger = getLogger("business")


class TenderManager:

    def __init__(self, announce_number, auth_data, *args, **kwargs) -> None:
        self.session_manager = GoszakupAuthorization(auth_data)
        self.web_driver: Chrome = self.session_manager.get_auth_session()
        self.webdriver_manager = WebDriverManager(self.web_driver)
        self.eds_manager = EdsManager(auth_data)
        self.announce_number: str = announce_number
        self.result = {"success": True, "start_time": datetime.now()}
        self.application_data: dict = auth_data.application_data.model_dump()
        self.announce_url = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )
        self.application_url = (
            f"https://v3bl.goszakup.gov.kz/ru/application/create/{announce_number}"
        )

    def start(self) -> dict:
        self.waiting_until_the_start()
        self.tender_start()
        self.fill_and_submit_application()
        required_docs_urls = self.get_required_docs_links()
        for url in required_docs_urls:
            self.generate_document(url)
            self.sign_document()
        self.next_page()
        self.apply_application()
        result = self.check_application_result()
        self.session_manager.close_session()
        return result

    def waiting_until_the_start(self) -> None:
        """Ждать до времени старта указанной в карте."""

        self.web_driver.get(self.announce_url)
        announce = self.web_driver.page_source
        announce_detail = self.gather_announce_data(announce)
        start_time_format = "%Y-%m-%d %H:%M:%S"
        start_time = datetime.strptime(announce_detail["start_time"], start_time_format)
        now = datetime.now()
        if start_time > now:
            wait_seconds = (start_time - now).total_seconds()
            logger.info(f"Waiting {wait_seconds} seconds for {self.announce_number}.")
            sleep(wait_seconds)
        business_logger.info(f"Starting tender at {datetime.now()} for {self.announce_number}")

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

    def fill_and_submit_application(self) -> None:
        """Заполнить необходимые поля заявки и подать заявку."""

        for field_name, search_text in self.application_data.items():
            select_element = self.web_driver.find_element(By.NAME, field_name)
            select = Select(select_element)
            for option in select.options:
                if search_text in option.text:
                    select.select_by_visible_text(option.text)
                    break
        next_button = self.web_driver.find_element(By.ID, "next-without-captcha")
        next_button.click()

    def get_required_docs_links(self) -> list:
        """Вернуть список ссылок на документы обязательных для подписания."""

        WebDriverWait(self.web_driver, 120).until(
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

    def generate_document(self, url) -> None:
        "Сформировать документ."

        self.web_driver.get(url)
        submit_button = self.web_driver.find_element(By.CSS_SELECTOR, ".btn.btn-info")
        submit_button.click()

    def sign_document(self) -> None:
        "Подписать документ ЭЦП."

        nclayer_call_btn = WebDriverWait(self.web_driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-add-signature"))
        )
        if self.eds_manager.is_not_busy():
            self.web_driver.execute_script("arguments[0].click();", nclayer_call_btn)
            self.eds_manager.execute_sign_by_eds("gos_eds")

    def next_page(self) -> None:
        "Вернуться к списку документов и нажать далее."

        while True:
            try:
                footer = WebDriverWait(self.web_driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "panel-footer"))
                )
                return_button = footer.find_element(By.TAG_NAME, "a")
                link = return_button.get_attribute("href")
                self.web_driver.get(link)
                break
            except (StaleElementReferenceException, TimeoutException):
                pass
        next_button = WebDriverWait(self.web_driver, 30).until(
            EC.element_to_be_clickable((By.ID, "next"))
        )
        next_button.click()

    def apply_application(self) -> None:
        "Нажать кнопку подать заявку."

        apply_button = WebDriverWait(self.web_driver, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='next' and contains(text(), 'Подать заявку')]")
            )
        )
        apply_button.click()
        yes_button = WebDriverWait(self.web_driver, 120).until(
            EC.element_to_be_clickable((By.ID, "btn_price_agree"))
        )
        yes_button.click()

    def check_application_result(self) -> dict:
        "После подтверждения может выйти ошибка."

        try:
            WebDriverWait(self.web_driver, 120).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(), 'Отозвать заявку')]")
                )
            )
            self.result["finish_time"] = datetime.now()
            self.result["duration"] = (
                self.result["finish_time"] - self.result["start_time"]
            )
            msg = f"Success finish tender at {datetime.now()} for {self.announce_number}"
            business_logger.info(msg)
        except TimeoutException:
            error = WebDriverWait(self.web_driver, 120).until(
                EC.element_to_be_clickable((By.ID, "errors"))
            )
            self.result["success"] = False
            self.result["error_text"] = error.text
            msg = f"Failed finish tender at {datetime.now()} for {self.announce_number}"
            business_logger.error(msg)            
        return self.result

    def check_announce(self) -> any:
        result = {"success": True}
        self.web_driver.get(self.announce_url)
        announce = self.web_driver.page_source
        announce_detail = self.gather_announce_data(announce)
        result.update(announce_detail)
        self.session_manager.close_session()
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
