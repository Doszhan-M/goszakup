import os
import ssl
import pyautogui
import pyperclip
import subprocess
from websocket import create_connection
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

    busy_timeout = 15

    def __init__(self, eds_data) -> None:
        self.eds_path = eds_data.eds_path
        self.eds_pass = eds_data.eds_pass

    def execute_sign_by_eds(self) -> None:
        try:
            redis.set("eds_manager_busy", 1, ex=self.busy_timeout)
            self.click_choose_btn()
            self.indicate_eds_path()
            self.click_open_btn()
            self.enter_eds_password()
            self.click_ok_btn()
        except Exception:
            logger.exception("Failed wile execute_sign_by_eds.")
            self.restart_ncalayer()

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
        timeout = 5
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

    @staticmethod
    def close_ncalayer_by_x() -> None:
        close_btn_path = pyautogui_images + "close_btn.png"
        timeout = 5
        start_time = time()
        while time() - start_time < timeout:
            try:
                close_btn_location = pyautogui.locateCenterOnScreen(
                    close_btn_path, confidence=0.8
                )
                pyautogui.click(close_btn_location)
                logger.info("close_ncalayer")
                return
            except pyautogui.ImageNotFoundException:
                pass

    @classmethod
    def restart_ncalayer(cls) -> None:
        try:
            redis.set("eds_manager_busy", 1, ex=cls.busy_timeout)
            script_path = os.path.expanduser(settings.NCALAYER_PATH)
            subprocess.run([script_path, "--restart"], check=True)
        except subprocess.CalledProcessError:
            logger.error("NCALayer перезапущен.")
            cls.healthcheck_ncalayer()
            redis.delete("eds_manager_busy")

    @classmethod
    def healthcheck_ncalayer(cls) -> None:
        try:
            uri = "wss://127.0.0.1:13579/"
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            websocket = create_connection(uri, sslopt={"cert_reqs": ssl.CERT_NONE})
            websocket.send("HealthCheck!")
            response = websocket.recv()
            if "result" in response:
                logger.info(f"NCALayer work properly!")
            websocket.close()
        except ConnectionRefusedError:
            logger.error("NCALayer dont work, waiting....")
            sleep(0.3)
            return cls.healthcheck_ncalayer()
