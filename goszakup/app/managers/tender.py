from time import sleep
from logging import getLogger
from selenium.webdriver.common.by import By

from .eds import EdsManager


logger = getLogger("fastapi")


class TenderManager(EdsManager):

    def __init__(self, announce_number, auth_data, *args, **kwargs) -> None:
        super().__init__(auth_data=auth_data, *args, **kwargs)
        self.auth_url = "https://v3bl.goszakup.gov.kz/ru/user/"

    def check_announce(self) -> any:
        
        self.web_driver.get(self.auth_url)
        eds_select = self.web_driver.find_element(By.ID, "selectP12File")
        self.execute_sign_by_eds("auth_eds", eds_select)
        
        sleep(5)
