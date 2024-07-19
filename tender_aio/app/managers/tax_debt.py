from time import sleep
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .auth import GoszakupAuth
from app.services import PlaywrightDriver


logger = getLogger("business")


class TaxDebtManager:

    def __init__(self, auth_data, delta, *args, **kwargs) -> None:
        self.session_manager = GoszakupAuth(auth_data)
        self.web_driver: Chrome = self.session_manager.get_auth_session()
        self.webdriver_manager = PlaywrightDriver(self.web_driver)
        self.tax_debt_url = "https://v3bl.goszakup.gov.kz/ru/cabinet/tax_debts"
        self.time_delta = delta
        self.result = {"success": True, "start_time": datetime.now()}

    def start(self) -> dict:
        self.web_driver.get(self.tax_debt_url)
        date_received = self.get_last_received_date()
        if datetime.now() - date_received > timedelta(days=self.time_delta):
            self.request_to_kgd()
            date_received = datetime.now()
        self.set_result(date_received)
        self.session_manager.close_session()
        return self.result

    def get_last_received_date(self) -> datetime:
        tax_debt = self.web_driver.page_source
        soup = BeautifulSoup(tax_debt, "html.parser")
        first_row = (
            soup.find("table", class_="table table-bordered").find("tbody").find("tr")
        )
        date_received_str = first_row.find_all("td")[3].text.strip()
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d %H:%M:%S")
        return date_received

    def request_to_kgd(self) -> None:
        button = WebDriverWait(self.web_driver, 120).until(
            EC.element_to_be_clickable((By.NAME, "send_request"))
        )
        button.click()
        sleep(5)

    def set_result(self, date_received) -> None:
        self.result["finish_time"] = datetime.now()
        self.result["last_received_date"] = date_received
        logger.info(f"Finish {self.__class__.__name__}! Last received: {date_received}")
