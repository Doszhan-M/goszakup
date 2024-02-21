import pyautogui
from time import sleep, time
from logging import getLogger

from app.schemas import AuthScheme
from app.core.config import settings


logger = getLogger("fastapi")
if settings.DEVELOPMENT:
    pyautogui_images = settings.BASE_DIR + "/static/pyautogui/images/dev/"
else:
    pyautogui_images = settings.BASE_DIR + "/static/pyautogui/images/prod/"
eds_manager_busy = False


class EdsManager:

    def __init__(self, auth_data: AuthScheme, *args, **kwargs) -> None:
        self.eds_auth = auth_data.eds_auth
        self.eds_gos = auth_data.eds_gos
        self.eds_pass = auth_data.eds_pass

    def execute_sign_by_eds(self, type_) -> None:
        self.click_choose_btn()
        self.indicate_eds_path(type_)
        self.click_open_btn()
        self.enter_eds_password()
        self.click_ok_btn()

    def is_not_busy(self):
        global eds_manager_busy
        while eds_manager_busy:
            logger.info("eds_manager_busy")
            sleep(0.1)
        eds_manager_busy = True
        return True

    def click_btn(self, btn_path, timeout=5) -> None:
        start_time = time() 
        button = None
        while not button and time() - start_time < timeout:
            try:
                button = pyautogui.locateOnScreen(btn_path, confidence=0.8)
            except pyautogui.ImageNotFoundException:
                sleep(0.1)
            else:
                pyautogui.click(button)

    def click_choose_btn(self) -> None:
        logger.info("click_choose_btn")
        choose_btn_path = pyautogui_images + "choose_btn.png"
        self.click_btn(choose_btn_path, 60)

    def indicate_eds_path(self, type_) -> None:
        logger.info("indicate_eds_path")
        if type_ == "auth_eds":
            eds_path = self.eds_auth
        else:
            eds_path = self.eds_gos
        pyautogui.write(eds_path)

    def click_open_btn(self) -> None:
        logger.info("click_open_btn")
        open_btn_path = pyautogui_images + "open_btn.png"
        self.click_btn(open_btn_path)

    def enter_eds_password(self) -> None:
        logger.info("enter_eds_password")
        pyautogui.write(self.eds_pass)

    def click_ok_btn(self) -> None:
        logger.info("click_ok_btn")
        open_btn_path = pyautogui_images + "ok_btn.png"
        self.click_btn(open_btn_path)
        global eds_manager_busy
        eds_manager_busy = False
