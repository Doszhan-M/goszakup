from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from app.core.config import settings


class WebDriverManager:

    def __init__(self, *args, **kwargs) -> None:
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.110 Safari/537.36"
        )
        options.add_argument("--window-size=1920,1200")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-proxy-server")
        if settings.IN_DOCKER:
            options.add_argument("--headless")  # off window
        # self.driver = webdriver.Chrome(options=options)

    def open_new_tab(self) -> webdriver.Chrome:
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            return self.driver
        except WebDriverException:
            self.__init__()
            return self.open_new_tab()

    def close_current_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


webdriver_manager = WebDriverManager()
