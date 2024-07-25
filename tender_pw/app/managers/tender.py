import re
import grpc
import asyncio
from logging import getLogger
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from app.pb2 import eds_pb2
from app.pb2 import eds_pb2_grpc
from .auth import GoszakupAuth
from app.core.config import settings
from .tender_cancel import TenderCancelManager
from app.services.exceptions import TenderStartFailed, SignatureFound

logger = getLogger("fastapi")
business_logger = getLogger("business")


class TenderManager:

    max_attempts = 3

    def __init__(self, announce_number, auth_data) -> None:
        self.session = GoszakupAuth(auth_data)
        self.page: Page = None
        self.cancel_manager = TenderCancelManager(announce_number, auth_data, self.page)
        self.announce_number: str = announce_number
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
                return await self.start()
            except Exception as e:
                logger.exception(
                    f"Attempt {attempt + 1} of {self.max_attempts} failed."
                )
                if attempt < self.max_attempts - 1:
                    await self.cancel_manager.cancel()
                    await self.session.close_session()
                else:
                    logger.exception("Task stopped with an error.")
                    await self.session.close_session()
                    self.result["success"] = False
                    self.result["finish_time"] = datetime.now()
                    self.result["error_text"] = e
                    return self.result
        await self.session.close_session()

    async def start(self) -> dict:
        self.page = await self.session.get_auth_session()
        await self.wait_until_the_start()
        await self.tender_start()
        self.result["start_time"] = datetime.now()
        await self.fill_and_submit_application()
        await self.select_lots()
        required_docs_urls = await self.get_required_docs_links()
        for url in required_docs_urls:
            try:
                await self.generate_document(url)
                await self.sign_document()
            except SignatureFound:
                continue
        await self.next_page()
        await self.apply_application()
        result = await self.check_application_result()
        return result

    async def wait_until_the_start(self) -> None:
        await self.page.goto(self.announce_url, wait_until="domcontentloaded")
        html = await self.page.content()
        announce_detail = self.gather_announce_data(html)
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
        await self.page.goto(self.application_url, wait_until="domcontentloaded")
        application = await self.page.content()
        soup = BeautifulSoup(application, "html.parser")
        elements = soup.find_all(class_="content-block")
        tender_not_starting = any(
            "Страница не найдена" in element.text for element in elements
        )
        if try_count == 0:
            raise TenderStartFailed(self.announce_number)
        elif tender_not_starting:
            await asyncio.sleep(0.1)
            try_count -= 1
            return await self.tender_start(try_count)

    async def fill_and_submit_application(self) -> None:
        current_url = self.page.url
        if "create" not in current_url:
            return
        for field_name, search_text in self.application_data.items():
            select_element = await self.page.query_selector(
                f"select[name='{field_name}']"
            )
            options = await select_element.query_selector_all("option")
            for option in options:
                option_text = await option.inner_text()
                if search_text in option_text:
                    option_value = await option.get_attribute("value")
                    await select_element.select_option(value=option_value)
                    break
        next_button = await self.page.query_selector("#next-without-captcha")
        await next_button.click()

    async def select_lots(self):
        await self.page.wait_for_url(re.compile(r".*(lots|docs|preview).*"))
        if "lots" not in self.page.url:
            return
        checkboxes = await self.page.query_selector_all(
            "input[type='checkbox'][name='selectLots[]']"
        )
        for checkbox in checkboxes:
            await checkbox.set_checked(True)
        add_button = await self.page.query_selector("button#add_lots")
        if add_button:
            await add_button.click()
        next_button = await self.page.wait_for_selector("button#next")
        if next_button:
            await next_button.click()

    async def get_required_docs_links(self) -> list:
        await self.page.wait_for_url(re.compile(r".*(docs|preview).*"))
        if "docs" not in self.page.url:
            return []
        await self.page.wait_for_selector("#docs")
        html = await self.page.content()
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
        await self.page.goto(url)
        submit_button = await self.page.query_selector(
            "input[type='submit'][value='Сформировать документ']"
        )
        if submit_button:
            await submit_button.click()
            return
        save_button = await self.page.query_selector(
            "input[type='submit'][value='Сохранить']"
        )
        if save_button:
            select_element = await self.page.query_selector("select[name='user_id']")
            if select_element:
                await select_element.select_option(index=1)
            await save_button.click()
            submit_button = await self.page.query_selector(
                "input[type='submit'][value='Сформировать документ']"
            )
            await submit_button.click()
            return
        signatures_table = await self.page.query_selector("table#show_doc_block1")
        if signatures_table:
            rows = await signatures_table.query_selector_all("tbody tr")
            for row in rows:
                cells = await row.query_selector_all("td")
                for cell in cells:
                    cell_text = await cell.inner_text()
                    if "Подпись" in cell_text:
                        raise SignatureFound("Signature found in the table")

    async def sign_document(self) -> None:
        nclayer_call_btn = await self.page.wait_for_selector(".btn-add-signature")
        async with grpc.aio.insecure_channel(settings.SIGNER_HOST) as channel:
            stub = eds_pb2_grpc.EdsServiceStub(channel)
            eds_manager_status = stub.SendStatus(eds_pb2.EdsManagerStatusCheck())
            async for status in eds_manager_status:
                if status.busy.value:
                    logger.info("Eds Service is busy. Waiting...")
            await nclayer_call_btn.click()
            eds_data = eds_pb2.SignByEdsStart(
                eds_path=self.session.auth_data.eds_gos,
                eds_pass=self.session.auth_data.eds_pass,
            )
            sign_by_eds = await stub.ExecuteSignByEds(eds_data)
            if sign_by_eds.result:
                await self.page.wait_for_timeout(1000)

    async def next_page(self) -> None:
        while True:
            try:
                footer = await self.page.wait_for_selector(
                    ".panel-footer a", timeout=5000
                )
                link = await footer.get_attribute("href")
                await self.page.goto(link)
                break
            except PlaywrightTimeoutError:
                pass
        next_button = await self.page.wait_for_selector("#next")
        await next_button.click()

    async def apply_application(self) -> None:
        apply_button = await self.page.wait_for_selector(
            "//button[@id='next' and contains(text(), 'Подать заявку')]"
        )
        await apply_button.click()
        yes_button = await self.page.wait_for_selector(
            "#modal_agree_price .btn.btn-info#btn_price_agree_no_captcha"
        )
        await yes_button.click()

    async def check_application_result(self) -> dict:
        try:
            await self.page.wait_for_selector(
                "//a[contains(text(), 'Отозвать заявку')]"
            )
            self.result["finish_time"] = datetime.now()
            self.result["duration"] = (
                self.result["finish_time"] - self.result["start_time"]
            )
            msg = (
                f"Success finish tender at {datetime.now()} for {self.announce_number}"
            )
            business_logger.info(msg)
        except PlaywrightTimeoutError:
            error = await self.page.query_selector("#errors")
            self.result["success"] = False
            self.result["error_text"] = await error.inner_text()
            msg = f"Failed finish tender at {datetime.now()} for {self.announce_number}"
            business_logger.error(msg)
        return self.result

    async def check_announce(self) -> any:
        self.page = await self.session.get_auth_session()
        await self.page.goto(self.announce_url, wait_until="domcontentloaded")
        html = await self.page.content()
        announce_detail = self.gather_announce_data(html)
        self.result.update(announce_detail)
        await self.session.close_session()
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
