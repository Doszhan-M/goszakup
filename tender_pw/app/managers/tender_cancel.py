from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .auth import GoszakupAuth
from app.services import PlaywrightDriver


class TenderCancelManager:

    def __init__(
        self, announce_number, auth_data, web_driver=None, *args, **kwargs
    ) -> None:
        self.web_driver = web_driver
        if not self.web_driver:
            self.session_manager = GoszakupAuth(auth_data)
            self.web_driver: Chrome = self.session_manager.get_auth_session()
        self.web_driver_wait = WebDriverWait(self.web_driver, 120)
        self.webdriver_manager = PlaywrightDriver(self.web_driver)
        self.announce_number: str = announce_number
        self.applications_url = "https://v3bl.goszakup.gov.kz/ru/myapp"

    def cancel(self) -> dict:
        self.web_driver.get(self.applications_url)
        self.click_cancel_btn()
        self.click_confirm_btn()

    def click_cancel_btn(self) -> None:
        link = self.web_driver_wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//a[contains(@href, '{self.announce_number}')]")
            )
        )
        row = link.find_element(By.XPATH, "./ancestor::tr")
        delete_button = row.find_element(By.XPATH, ".//a[contains(@onclick, 'doDel')]")
        delete_button.click()

    def click_confirm_btn(self) -> None:
        delete_button_in_modal = self.web_driver_wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and contains(., 'Удалить')]")
            )
        )
        delete_button_in_modal.click()

    def close_session(self):
        self.session_manager.close_session()
