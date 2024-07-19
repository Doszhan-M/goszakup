import asyncio
from time import sleep
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from .auth import GoszakupAuth
# from .tender_cancel import TenderCancelManager
from app.services import PlaywrightDriver
from app.services.exception import TenderStartFailed, GenerateDocumentFailed
from app.pb2 import eds_pb2
from app.pb2 import eds_pb2_grpc

logger = getLogger("fastapi")
business_logger = getLogger("business")

class TenderManager:
    def __init__(self, announce_number, auth_data, *args, **kwargs) -> None:
        self.session_manager = GoszakupAuth(auth_data)
        self.web_driver: Page = None
        self.webdriver_manager = PlaywrightDriver()
        # self.cancel_manager = TenderCancelManager(
        #     announce_number, auth_data, self.web_driver
        # )
        self.announce_number: str = announce_number
        self.max_attempts = 3
        self.result = {"success": True}
        self.application_data: dict = auth_data.application_data.model_dump()
        self.announce_url = (
            f"https://v3bl.goszakup.gov.kz/ru/announce/index/{announce_number}"
        )
        self.application_url = (
            f"https://v3bl.goszakup.gov.kz/ru/application/create/{announce_number}"
        )

    async def start_with_retry(self):
        for attempt in range(self.max_attempts):
            try:
                result = await self.start()
                return result
            except Exception as e:
                logger.error(e)
                logger.error(f"Attempt {attempt + 1} of {self.max_attempts} failed.")
                if attempt < self.max_attempts - 1:
                    delay = 2
                    logger.error(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    await self.cancel_manager.cancel()
                else:
                    logger.error("Task stopped with an error.")
                    await self.session_manager.close_session()
                    self.result["success"] = False
                    self.result["finish_time"] = datetime.now()
                    self.result["error_text"] = e
                    return self.result

    async def check_announce(self) -> any:
        self.web_driver = await self.session_manager.get_auth_session()
        
        result = {"success": True}
        await self.web_driver.goto(self.announce_url)
        announce = await self.web_driver.content()
        announce_detail = self.gather_announce_data(announce)
        result.update(announce_detail)
        await self.session_manager.close_session()
        return result
    
    async def start(self) -> dict:
        await self.waiting_until_the_start()
        await self.tender_start()
        self.result["start_time"] = datetime.now()
        await self.fill_and_submit_application()
        required_docs_urls = await self.get_required_docs_links()
        for url in required_docs_urls:
            await self.generate_document(url)
            await self.sign_document()
        await self.next_page()
        await self.apply_application()
        result = await self.check_application_result()
        await self.session_manager.close_session()
        return result

    async def waiting_until_the_start(self) -> None:
        await self.web_driver.goto(self.announce_url)
        announce = await self.web_driver.content()
        announce_detail = self.gather_announce_data(announce)
        start_time_format = "%Y-%m-%d %H:%M:%S"
        start_time = datetime.strptime(announce_detail["start_time"], start_time_format)
        now = datetime.now()
        if start_time > now:
            wait_seconds = (start_time - now).total_seconds()
            logger.info(f"Waiting {wait_seconds} seconds for {self.announce_number}.")
            await asyncio.sleep(wait_seconds)
        business_logger.info(
            f"Starting tender at {datetime.now()} for {self.announce_number}"
        )

    async def tender_start(self, try_count=3600) -> None:
        await self.web_driver.goto(self.application_url)
        application = await self.web_driver.content()
        soup = BeautifulSoup(application, "html.parser")
        elements = soup.find_all(class_="content-block")
        tender_not_starting = any(
            "Страница не найдена" in element.text for element in elements
        )
        if try_count == 0:
            raise TenderStartFailed(self.announce_number)
        elif tender_not_starting:
            await asyncio.sleep(1)
            try_count -= 1
            return await self.tender_start(try_count)

    async def fill_and_submit_application(self) -> None:
        for field_name, search_text in self.application_data.items():
            select_element = await self.web_driver.query_selector(f"select[name='{field_name}']")
            options = await select_element.query_selector_all("option")
            for option in options:
                if search_text in await option.inner_text():
                    await select_element.select_option(label=await option.inner_text())
                    break
        next_button = await self.web_driver.query_selector("#next-without-captcha")
        await next_button.click()

    async def get_required_docs_links(self) -> list:
        await self.web_driver.wait_for_selector("#docs", timeout=120000)
        html = await self.web_driver.content()
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        required_docs = []
        for row in rows:
            if "Не Обязателен" not in row.text:
                link = row.find("a", href=True)
                if link:
                    required_docs.append(link["href"])
        return required_docs

    async def generate_document(self, url) -> None:
        await self.web_driver.goto(url)
        submit_button = await self.web_driver.query_selector(".btn.btn-info")
        submit_button_value = await submit_button.get_attribute("value")
        if submit_button_value != "Сформировать документ":
            self.max_attempts = 1
            raise GenerateDocumentFailed
        await submit_button.click()

    async def sign_document(self) -> None:
        nclayer_call_btn = await self.web_driver.wait_for_selector(".btn-add-signature", timeout=120000)
        async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
            stub = eds_pb2_grpc.EdsServiceStub(channel)
            eds_manager_status = stub.SendStatus(eds_pb2.EdsManagerStatusCheck())
            async for status in eds_manager_status:
                if status.busy.value:
                    logger.info("Eds Service is busy. Waiting...")
            await nclayer_call_btn.click()
            eds_data = eds_pb2.SignByEdsStart(
                eds_path=self.eds_manager.auth_data.eds_gos,
                eds_pass=self.eds_manager.auth_data.eds_pass,
            )
            sign_by_eds = await stub.ExecuteSignByEds(eds_data)
            if sign_by_eds.result:
                await self.web_driver.wait_for_timeout(1000)

    async def next_page(self) -> None:
        while True:
            try:
                footer = await self.web_driver.wait_for_selector(".panel-footer a", timeout=5000)
                link = await footer.get_attribute("href")
                await self.web_driver.goto(link)
                break
            except PlaywrightTimeoutError:
                pass
        next_button = await self.web_driver.wait_for_selector("#next", timeout=30000)
        await next_button.click()

    async def apply_application(self) -> None:
        apply_button = await self.web_driver.wait_for_selector(
            "//button[@id='next' and contains(text(), 'Подать заявку')]", timeout=120000
        )
        await apply_button.click()
        yes_button = await self.web_driver.wait_for_selector("#btn_price_agree", timeout=120000)
        await yes_button.click()

    async def check_application_result(self) -> dict:
        try:
            await self.web_driver.wait_for_selector("//a[contains(text(), 'Отозвать заявку')]", timeout=120000)
            self.result["finish_time"] = datetime.now()
            self.result["duration"] = (
                self.result["finish_time"] - self.result["start_time"]
            )
            msg = (
                f"Success finish tender at {datetime.now()} for {self.announce_number}"
            )
            business_logger.info(msg)
        except PlaywrightTimeoutError:
            error = await self.web_driver.query_selector("#errors")
            self.result["success"] = False
            self.result["error_text"] = await error.inner_text()
            msg = f"Failed finish tender at {datetime.now()} for {self.announce_number}"
            business_logger.error(msg)
        return self.result



    def gather_announce_data(self, raw_data) -> dict:
        announce_detail = {}
        targets_and_label_texts = [
            ("announce_name", "Наименование объявления"),
            ("announce_status", "Статус объявления"),
            ("start_time", "Срок начала приема заявок"),
            ("finish_time", "Срок окончания приема заявок"),
        ]
        soup = BeautifulSoup(raw_data, "html.parser")
        labels = soup.find_all("label")
        for label in labels:
            for key, label_text in targets_and_label_texts:
                if label_text in label.text:
                    next_input = label.find_next("input")
                    input_value = next_input.get("value")
                    announce_detail[key] = input_value
        return announce_detail