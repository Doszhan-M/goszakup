import pyautogui
import pyperclip
from time import sleep, time
from logging import getLogger

from services import get_redis
from core.config import settings


logger = getLogger("grpc")
redis = get_redis()


if settings.ENVIRONMENT == "TUF17":
    pyautogui_images = settings.BASE_DIR + "/static/tuf17/"
elif settings.ENVIRONMENT == "VIVOBOOK":
    pyautogui_images = settings.BASE_DIR + "/static/vivobook/"


class EdsManager:
    def __init__(self, eds_data) -> None:
        self.eds_path = eds_data.eds_path
        self.eds_pass = eds_data.eds_pass

    def execute_sign_by_eds(self) -> None:
        try:
            self.move_cursor_to_bottom_left()
            import time
            time.sleep(5)
            raise Exception
            # redis.set("eds_manager_busy", 1, ex=10)
            # self.click_choose_btn()
            # self.indicate_eds_path()
            # self.click_open_btn()
            # self.enter_eds_password()
            # self.click_ok_btn()
        except Exception:
            logger.exception("Error while execute_sign_by_eds")
            self.close_ncalayer()

    @staticmethod
    def is_not_busy() -> bool:
        while redis.get("eds_manager_busy"):
            logger.info("eds manager busy")
            sleep(0.1)
        return True

    def click_btn(self, btn_path: str, timeout=5) -> None:
        start_time = time()
        button = None
        while not button and time() - start_time < timeout:
            try:
                button = pyautogui.locateOnScreen(btn_path, confidence=0.8)
            except pyautogui.ImageNotFoundException:
                pass
            else:
                pyautogui.click(button)
                logger.info(f"click {btn_path.split('/')[-1]}")
        if not button:
            logger.error(f"not found {btn_path.split('/')[-1]}")

    def click_choose_btn(self) -> None:
        choose_btn_path = pyautogui_images + "choose_btn.png"
        form_exist_path = pyautogui_images + "form_exist.png"
        timeout = 10
        start_time = time()
        while time() - start_time < timeout:
            try:
                choose_btn_location = pyautogui.locateCenterOnScreen(
                    choose_btn_path, confidence=0.8
                )
                pyautogui.click(choose_btn_location)
                return
            except pyautogui.ImageNotFoundException:
                pass
            try:
                pyautogui.locateCenterOnScreen(form_exist_path, confidence=0.8)
                return
            except pyautogui.ImageNotFoundException:
                pass
        raise Exception(f"Neither button found within {timeout} seconds.")

    def indicate_eds_path(self) -> None:
        pyperclip.copy(self.eds_path)
        pyautogui.hotkey("ctrl", "v")
        logger.info("enter_eds_path")

    def click_open_btn(self) -> None:
        open_btn_path = pyautogui_images + "open_btn.png"
        self.click_btn(open_btn_path)

    def enter_eds_password(self) -> None:
        pyperclip.copy(self.eds_pass)
        pyautogui.hotkey("ctrl", "v")
        logger.info("enter_eds_password")

    def click_ok_btn(self) -> None:
        open_btn_path = pyautogui_images + "ok_btn.png"
        self.click_btn(open_btn_path)
        redis.delete("eds_manager_busy")

    def move_cursor_to_bottom_left(self):
        """Если экран выключен, pyautogui не работает, поэтому
        необходимо разбудить экран переместив мышку из одного места в другое."""

        screen_width, screen_height = pyautogui.size()
        safe_margin = 400
        pyautogui.moveTo(safe_margin, screen_height - safe_margin)

    def close_ncalayer(self) -> None:
        close_btn_path = pyautogui_images + "close_btn.png"
        print('close_btn_path: ', close_btn_path)
        timeout = 10
        start_time = time()
        while time() - start_time < timeout:
            try:
                close_btn_location = pyautogui.locateCenterOnScreen(
                    close_btn_path, confidence=0.8
                )
                print('close_btn_location: ', close_btn_location)
                pyautogui.click(close_btn_location)
                logger.info("close_ncalayer")
                return
            except pyautogui.ImageNotFoundException:
                pass
