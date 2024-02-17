from logging import getLogger
from selenium.webdriver import Chrome
from time import sleep
import pyautogui

from app.schemas import AuthScheme
from app.services import webdriver_manager


logger = getLogger("fastapi")
eds_manager_busy = False


class EdsManager:

    def __init__(self, auth_data: AuthScheme, *args, **kwargs) -> None:
        self.eds_auth = auth_data.eds_auth
        self.eds_gos = auth_data.eds_gos
        self.eds_pass = auth_data.eds_pass
        self.goszakup_pass = auth_data.goszakup_pass

    def __enter__(self):

        self.webdriver_manager = webdriver_manager
        self.web_driver: Chrome = self.webdriver_manager.open_new_tab()
        self.web_driver.implicitly_wait(10)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("finish TenderManager")
        self.webdriver_manager.close_current_tab()

    def execute_sign_by_eds(self, type_, call_bnt) -> None:
        self.call_nclayer(call_bnt)
        self.click_choose_btn()
        self.indicate_eds_path(type_)
        self.click_open_btn()
        self.enter_eds_password()
        self.click_ok_btn()

    def call_nclayer(self, call_bnt):
        global eds_manager_busy
        while eds_manager_busy:
            logger.info("eds_manager_busy")
            sleep(0.1)
        call_bnt.click()
        eds_manager_busy = True

    def click_btn(self, btn_path) -> None:
        button = None
        while not button:
            try:
                button = pyautogui.locateOnScreen(btn_path, confidence=0.8)
            except pyautogui.ImageNotFoundException:
                sleep(0.1)
            else:
                pyautogui.click(button)

    def click_choose_btn(self) -> None:
        logger.info("click_choose_btn")
        choose_btn_path = (
            "/home/asus/github/goszakup/goszakup/app/static/img/choose_btn.png"
        )
        self.click_btn(choose_btn_path)

    def indicate_eds_path(self, type_) -> None:
        logger.info("indicate_eds_path")
        if type_ == "auth_eds":
            eds_path = self.eds_auth
        else:
            eds_path = self.eds_gos
        pyautogui.write(eds_path)

    def click_open_btn(self) -> None:
        logger.info("click_open_btn")
        open_btn_path = (
            "/home/asus/github/goszakup/goszakup/app/static/img/open_btn.png"
        )
        self.click_btn(open_btn_path)

    def enter_eds_password(self) -> None:
        logger.info("enter_eds_password")
        pyautogui.write(self.eds_pass)

    def click_ok_btn(self) -> None:
        logger.info("click_ok_btn")
        open_btn_path = "/home/asus/github/goszakup/goszakup/app/static/img/ok_btn.png"
        self.click_btn(open_btn_path)
        global eds_manager_busy
        eds_manager_busy = False
