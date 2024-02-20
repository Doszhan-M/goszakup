from logging import getLogger
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from fastapi import Depends

from .eds import EdsManager
from app.schemas import AuthScheme


logger = getLogger("fastapi")
active_sessions = {}


class GoszakupAuthorization(EdsManager):
    """Manager for getting cookie from sud.kz."""

    def __init__(self, auth_data, session=None, *args, **kwargs):
        super().__init__(auth_data=auth_data, session=session, *args, **kwargs)
        self.auth_url = "https://v3bl.goszakup.gov.kz/ru/user/"
        self.zero_page = "https://v3bl.goszakup.gov.kz/ru/insurance"
        self.iin_bin: str = auth_data.iin_bin
        self.session_expire = 60

    def check_auth(self) -> any:
        try:
            current_tab_id = self.web_driver.current_window_handle
            self.webdriver_manager.switch_to_zero_tab()
            WebDriverWait(self.web_driver, 3).until(
                EC.presence_of_element_located((By.ID, "navbar-second"))
            )
            all_tabs = self.web_driver.window_handles
            for tab in all_tabs:
                if tab == current_tab_id:
                    self.web_driver.switch_to.window(tab)
        except TimeoutException:
            self.login_goszakup()
        return self.web_driver

    def login_goszakup(self) -> any:
        self.web_driver.get(self.auth_url)
        eds_select = self.web_driver.find_element(By.ID, "selectP12File")
        self.execute_sign_by_eds("auth_eds", eds_select)
        self.enter_goszakup_password()
        self.set_auth_session_in_zero_tab()
        self.store_auth_session()
        return self.web_driver

    def store_auth_session(self) -> None:
        global active_sessions
        delta = timedelta(minutes=self.session_expire)
        session = {"session": self.web_driver, "expire": datetime.now() + delta}
        active_sessions[self.iin_bin] = session
        logger.info(f"Store new session for {self.iin_bin}")

    def set_auth_session_in_zero_tab(self):
        current_tab_id = self.web_driver.current_window_handle
        self.webdriver_manager.switch_to_zero_tab()
        self.web_driver.get(self.zero_page)
        self.web_driver.refresh()
        all_tabs = self.web_driver.window_handles
        for tab in all_tabs:
            if tab == current_tab_id:
                self.web_driver.switch_to.window(tab)

    def enter_goszakup_password(self):
        password_field = self.web_driver.find_element(By.NAME, "password")
        password_field.send_keys(self.goszakup_pass)
        checkbox = self.web_driver.find_element(By.ID, "agreed_check")
        if not checkbox.is_selected():
            checkbox.click()
        login_button = self.web_driver.find_element(By.CLASS_NAME, "btn-success")
        login_button.click()


def get_auth_session(auth_data: AuthScheme = Depends()) -> any:
    global active_sessions
    auth_session = active_sessions.get(auth_data.iin_bin)
    if auth_session:
        session = auth_session["session"]
        with GoszakupAuthorization(auth_data, session) as manager:
            session = manager.check_auth()
    if not auth_session:
        with GoszakupAuthorization(auth_data) as manager:
            session = manager.login_goszakup()
    return session
