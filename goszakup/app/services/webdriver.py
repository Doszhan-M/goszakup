from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def web_driver():
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.110 Safari/537.36"
    )
    # options.add_argument("--headless")  # off window
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-proxy-server")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)
    return driver


def get_web_driver():
    driver = web_driver()
    try:
        yield driver
    finally:
        driver.close()
        driver.quit()
