from time import sleep
from logging import getLogger
from selenium.webdriver.common.by import By

from .eds import EdsManager


logger = getLogger("fastapi")


class TenderManager(EdsManager):

    def __init__(self, auth_session, announce_number, auth_data, *args, **kwargs) -> None:
        super().__init__(auth_data=auth_data, session=auth_session, *args, **kwargs)
        self.announce_number = announce_number
        self.announce_url: str = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )
    def check_announce(self) -> any:
        self.waiting_until_the_start()

    def waiting_until_the_start(self) -> None:
        """Ждать до времени старта указанной в карте."""

        announce = self.web_driver.get(self.announce_url)
        sleep(5)
        # announce_detail = self.gather_announce_data(announce)
        # # announce_detail["start_time"] = "2024-02-15 22:29:00"
        # start_time_format = "%Y-%m-%d %H:%M:%S"
        # start_time = datetime.strptime(announce_detail["start_time"], start_time_format)
        # now = datetime.now()
        # if start_time > now:
        #     wait_seconds = (start_time - now).total_seconds()
        #     logger.info(f"Waiting for {wait_seconds} seconds.")
        #     await asyncio.sleep(wait_seconds)
        # logger.info(f"Start tender {datetime.now()}")
