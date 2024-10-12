import os
import ssl
import shutil
import pyautogui
import pyperclip
import subprocess
from websocket import create_connection
from time import sleep, time
from logging import getLogger

from services import redis_lock, get_redis
from core.config import settings
from services.exceptions import ProjectError


logger = getLogger("grpc")
redis = get_redis()


if settings.ENVIRONMENT == "TUF17":
    pyautogui_images = settings.BASE_DIR + "/static/tuf17/"
elif settings.ENVIRONMENT == "VIVOBOOK":
    xvfb_1 = settings.BASE_DIR + "/static/server_gnome/"
    xvfb_2 = settings.BASE_DIR + "/static/vivobook/"
    pyautogui_images = xvfb_1    
elif settings.ENVIRONMENT == "SERVER_GNOME":
    xvfb_1 = settings.BASE_DIR + "/static/server_gnome/"
    xvfb_2 = settings.BASE_DIR + "/static/server_gnome_3/"
    pyautogui_images = xvfb_1


class EdsManager:

    busy_timeout = 15

    def __init__(self, eds_data) -> None:
        self.eds_path = eds_data.eds_path
        self.eds_pass = eds_data.eds_pass

    def execute_sign_by_eds(self) -> None:
        with redis_lock("eds_manager_busy", lock_timeout=self.busy_timeout):
            try:
                self.click_choose_btn()
                self.indicate_eds_path()
                self.click_open_btn()
                self.click_password_form()
                self.enter_eds_password()
                self.click_ok_btn()
            except (Exception, ProjectError):
                logger.exception("Failed wile execute_sign_by_eds.")
                self.restart_ncalayer(with_lock=False)

    @classmethod
    def is_not_busy(cls) -> bool:
        """
        Проверяет, занята ли система (т.е. установлена ли блокировка).
        Возвращает True, если не занята, иначе False.
        """
        is_locked = redis.exists("eds_manager_busy")
        return not is_locked

    def click_obj(self, btn_path: str, timeout=5) -> None:
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
            raise pyautogui.ImageNotFoundException

    def click_choose_btn(self) -> None:
        global pyautogui_images, xvfb_1, xvfb_2
        timeout = 5
        start_time = time()
        while time() - start_time < timeout:
            try:
                file_system_btn_path = pyautogui_images + "file_system_btn.png"
                self.click_obj(file_system_btn_path, timeout=1)
                return
            except pyautogui.ImageNotFoundException:
                pass
            try:
                form_exist_path = pyautogui_images + "form_exist.png"
                self.click_obj(form_exist_path)
                return
            except pyautogui.ImageNotFoundException:
                if pyautogui_images == xvfb_1:
                    pyautogui_images = xvfb_2
                    logger.warning("Switched pyautogui_images to xvfb_2")
                else:
                    pyautogui_images = xvfb_1
                    logger.warning("Switched pyautogui_images to xvfb_1")     

        raise ProjectError(f"Neither button found within {timeout} seconds.")

    def indicate_eds_path(self) -> None:
        pyperclip.copy(self.eds_path)
        pyautogui.hotkey("ctrl", "v")
        logger.info("enter_eds_path")

    def click_open_btn(self) -> None:
        global pyautogui_images
        open_btn_path = pyautogui_images + "open_btn.png"
        self.click_obj(open_btn_path)

    def click_password_form(self) -> None:
        global pyautogui_images
        password_form = pyautogui_images + "password_form.png"
        self.click_obj(password_form)

    def enter_eds_password(self) -> None:
        pyperclip.copy(self.eds_pass)
        pyautogui.hotkey("ctrl", "v")
        logger.info("enter_eds_password")

    def click_ok_btn(self) -> None:
        global pyautogui_images
        open_btn_path = pyautogui_images + "ok_btn.png"
        self.click_obj(open_btn_path)

    def move_cursor_to_bottom_left(self):
        """Если экран выключен, pyautogui не работает, поэтому
        необходимо разбудить экран переместив мышку из одного места в другое."""

        screen_width, screen_height = pyautogui.size()
        safe_margin = 400
        pyautogui.moveTo(safe_margin, screen_height - safe_margin)

    @classmethod
    def restart_ncalayer(cls, with_lock=True) -> None:
        if with_lock:
            with redis_lock("eds_manager_busy", lock_timeout=cls.busy_timeout):
                cls._restart_ncalayer()
        else:
            cls._restart_ncalayer()
            
    @classmethod
    def _restart_ncalayer(cls) -> None:
        logger.info("restart_ncalayer.")
        try:
            # Удалить папку ncalayer-cache
            cache_dir = "~/.config/NCALayer/ncalayer-cache"
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                logger.info(f"Ncalayer сброшен: {cache_dir}")
            # Скопировать плагин
            source_file = "~/github/goszakup/scripts/files/kz.ecc.NurSignBundle_5.1.1_2e62beae-e900-4c8c-9d8e-37286ace46ec.jar"
            dest_dir = "~/.config/NCALayer/bundles"
            os.makedirs(dest_dir, exist_ok=True)  # Создаем папку, если не существует
            shutil.copy(source_file, dest_dir)
            logger.info(f"Плагин скопирован: {source_file} -> {dest_dir}")
            
            script_path = os.path.expanduser(settings.NCALAYER_PATH)
            env = os.environ.copy()
            env['DISPLAY'] = ':99'
            subprocess.run([script_path, "--restart"], check=True, env=env)
        except subprocess.CalledProcessError:
            logger.error("NCALayer перезапущен.")
            cls.healthcheck_ncalayer()

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
                logger.info("NCALayer work properly!")
                sleep(1)
            websocket.close()
        except ConnectionRefusedError:
            logger.error("NCALayer dont work, waiting....")
            sleep(0.2)
            return cls.healthcheck_ncalayer()
