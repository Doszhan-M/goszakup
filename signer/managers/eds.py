import pyautogui
import pyperclip
from time import sleep, time
from logging import getLogger

from core.config import settings


logger = getLogger("grpc")
eds_manager_busy = False


if settings.ENVIRONMENT == "TUF17":
    pyautogui_images = settings.BASE_DIR + "/static/tuf17/"
elif settings.ENVIRONMENT == "VIVOBOOK":
    pyautogui_images = settings.BASE_DIR + "/static/vivobook/"


class EdsManager:
    def __init__(self, eds_data, *args, **kwargs) -> None:
        self.eds_path = eds_data.eds_path
        self.eds_pass = eds_data.eds_pass

    def execute_sign_by_eds(self) -> None:
        global eds_manager_busy
        eds_manager_busy = True
        self.click_choose_btn()
        self.indicate_eds_path()
        self.click_open_btn()
        self.enter_eds_password()
        self.click_ok_btn()

    @staticmethod
    def is_not_busy() -> bool:
        global eds_manager_busy
        while eds_manager_busy:
            logger.info("eds manager busy")
            sleep(0.1)
        return True

    def click_btn(self, btn_path: str, timeout=5) -> None:
        start_time = time()
        button = None
        while not button and time() - start_time < timeout:
            try:
                button = pyautogui.locateOnScreen(btn_path, confidence=0.7)
            except pyautogui.ImageNotFoundException:
                sleep(0.1)
            else:
                pyautogui.click(button)
                logger.info(f"click {btn_path.split('/')[-1]}")
        if not button:
            logger.error(f"not found {btn_path.split('/')[-1]}")

    def click_choose_btn(self) -> None:
        choose_btn_path = pyautogui_images + "choose_btn.png"
        print('choose_btn_path: ', choose_btn_path)
        self.click_btn(choose_btn_path, 60)

    def indicate_eds_path(self) -> None:
        # На некоторых средах write вставляет только по символьно
        pyperclip.copy(self.eds_path)
        pyautogui.hotkey("ctrl", "v")
        # pyautogui.write(eds_path)
        logger.info("enter_eds_path")

    def click_open_btn(self) -> None:
        open_btn_path = pyautogui_images + "open_btn.png"
        self.click_btn(open_btn_path)

    def enter_eds_password(self) -> None:
        pyperclip.copy(self.eds_pass)
        pyautogui.hotkey("ctrl", "v")
        # pyautogui.write(self.eds_pass)
        logger.info("enter_eds_password")

    def click_ok_btn(self) -> None:
        open_btn_path = pyautogui_images + "ok_btn.png"
        self.click_btn(open_btn_path)
        global eds_manager_busy
        eds_manager_busy = False
