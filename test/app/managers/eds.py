import os
import shutil
import requests
import pyautogui
import pyperclip
from time import sleep, time
from logging import getLogger

from services import redis_lock, get_redis
from core.config import settings
from services.exceptions import ProjectError


logger = getLogger("grpc")
redis = get_redis()


if settings.ENVIRONMENT == "TUF17":
    xvfb_1 = settings.BASE_DIR + "/static/tuf17_2/"
    xvfb_2 = settings.BASE_DIR + "/static/tuf17_2/"
    pyautogui_images = xvfb_1     
elif settings.ENVIRONMENT == "VIVOBOOK":
    xvfb_1 = settings.BASE_DIR + "/static/server_gnome/"
    xvfb_2 = settings.BASE_DIR + "/static/vivobook/"
    pyautogui_images = xvfb_1    
elif settings.ENVIRONMENT == "SERVER_GNOME":
    xvfb_1 = settings.BASE_DIR + "/static/server_gnome/"
    xvfb_2 = settings.BASE_DIR + "/static/server_gnome_3/"
    pyautogui_images = xvfb_1
elif settings.ENVIRONMENT == "DOCKER":
    xvfb_1 = settings.BASE_DIR + "/static/docker_1/"
    xvfb_2 = settings.BASE_DIR + "/static/docker_1/"
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
        """Проверяет, занята ли система (т.е. установлена ли блокировка)."""
        
        lock = redis.exists("eds_manager_busy")
        print('lock: ', lock)
        # if not lock:
        #     cls.healthcheck_ncalayer()
        return not lock

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

    def take_screenshot(self):
        from datetime import datetime
        print('settings.ENVIRONMENT: ', settings.ENVIRONMENT)
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"/app/screenshot_{timestamp}.png"
        screenshot.save(screenshot_path)
        print(f"Скриншот сохранен по пути: {screenshot_path}") 
                
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
        url = "http://host.docker.internal:9000/ncalayer/healthcheck?display=99"
        response = requests.get(url)
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("NCALayer work properly!")

    @classmethod
    def healthcheck_ncalayer(cls) -> None:
        url = "http://host.docker.internal:9000/ncalayer/healthcheck"
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("NCALayer work properly!")
