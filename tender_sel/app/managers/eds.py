import pyautogui
import pyperclip
from time import sleep, time
from logging import getLogger

from app.schemas import AuthScheme
from app.core.config import settings


logger = getLogger("fastapi")
eds_manager_busy = False
if settings.ENVIRONMENT == "TUF17":
    pyautogui_images = settings.BASE_DIR + "/static/pyautogui/images/tuf17/"
elif settings.ENVIRONMENT == "vivobook":
    pyautogui_images = settings.BASE_DIR + "/static/pyautogui/images/vivobook/"


class EdsManager:

    def __init__(self, auth_data: AuthScheme, *args, **kwargs) -> None:
        self.eds_gos = auth_data.eds_gos
        self.eds_pass = auth_data.eds_pass

    def execute_sign_by_eds(self, type_) -> None:
        # self.move_cursor_to_corner()
        self.click_choose_btn()
        # self.find_eds_path_form()
        self.indicate_eds_path(type_)
        self.click_open_btn()
        # self.find_pass_form()
        self.enter_eds_password()
        self.click_ok_btn()

    def move_cursor_to_corner(self) -> None:
        "Переместить курсор на край стола."

        pyautogui.FAILSAFE = False
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width - 100, screen_height - 100)

    def is_not_busy(self) -> bool:
        global eds_manager_busy
        while eds_manager_busy:
            logger.info("eds_manager_busy")
            sleep(0.1)
        eds_manager_busy = True
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
        self.click_btn(choose_btn_path, 60)

    def find_eds_path_form(self) -> None:
        form_path = pyautogui_images + "eds_form.png"
        self.click_btn(form_path, 30)
        
    def find_pass_form(self) -> None:
        form_path = pyautogui_images + "pass_form.png"
        self.click_btn(form_path, 30)
        
    def indicate_eds_path(self, type_) -> None:
        eds_path = self.eds_gos
        # На некоторых средах write вставляет только по символьно
        pyperclip.copy(eds_path) 
        pyautogui.hotkey('ctrl', 'v')
        # pyautogui.write(eds_path)
        logger.info("enter_eds_path")

    def click_open_btn(self) -> None:
        open_btn_path = pyautogui_images + "open_btn.png"
        self.click_btn(open_btn_path)

    def enter_eds_password(self) -> None:
        pyperclip.copy(self.eds_pass) 
        pyautogui.hotkey('ctrl', 'v')        
        # pyautogui.write(self.eds_pass)
        logger.info("enter_eds_password")

    def click_ok_btn(self) -> None:
        open_btn_path = pyautogui_images + "ok_btn.png"
        self.click_btn(open_btn_path)
        global eds_manager_busy
        eds_manager_busy = False