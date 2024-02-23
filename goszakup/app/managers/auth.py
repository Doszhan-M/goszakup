from uuid import uuid4
from time import sleep
from logging import getLogger
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By



from .eds import EdsManager
from app.services import WebDriverManager


logger = getLogger("fastapi")
active_sessions = {}


class GoszakupAuthorization():
    """Manager for getting cookie from sud.kz."""

    def __init__(self, auth_data, *args, **kwargs):
        self.webdriver_manager = WebDriverManager()
        self.web_driver:Chrome = self.webdriver_manager.start_window()
        self.web_driver.implicitly_wait(10)
        self.eds_manager = EdsManager(auth_data)
        self.auth_url = "https://v3bl.goszakup.gov.kz/ru/user/"
        self.zero_page = "https://v3bl.goszakup.gov.kz/ru/insurance"
        self.goszakup_pass = auth_data.goszakup_pass
        self.ssid = uuid4()

    def get_auth_session(self) -> Chrome:
        self.web_driver.get(self.auth_url)
        nclayer_call_btn = self.web_driver.find_element(By.ID, "selectP12File")
        if self.eds_manager.is_not_busy():
            nclayer_call_btn.click()
            self.eds_manager.execute_sign_by_eds("auth_eds")
            sleep(1)
        self.enter_goszakup_password()
        self.store_auth_session()
        return self.web_driver

    def enter_goszakup_password(self) -> None:
        password_field = self.web_driver.find_element(By.NAME, "password")
        password_field.send_keys(self.goszakup_pass)
        checkbox = self.web_driver.find_element(By.ID, "agreed_check")
        if not checkbox.is_selected():
            checkbox.click()
        login_button = self.web_driver.find_element(By.CLASS_NAME, "btn-success")
        login_button.click()

    def store_auth_session(self) -> None:
        global active_sessions
        active_sessions[self.ssid] = self.web_driver
        logger.info(f"Store new session id: {self.ssid}")

    def close_session(self):
        self.webdriver_manager.quite_window()
        del active_sessions[self.ssid]
