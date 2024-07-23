from logging import getLogger
from bs4 import BeautifulSoup
from playwright.async_api import Page
from datetime import datetime, timedelta

from .auth import GoszakupAuth


logger = getLogger("business")


class TaxDebtManager:

    tax_debt_url = "https://v3bl.goszakup.gov.kz/ru/cabinet/tax_debts"

    def __init__(self, auth_data, delta, *args, **kwargs) -> None:
        self.session = GoszakupAuth(auth_data)
        self.page: Page = None
        self.time_delta = delta
        self.result = {"success": True, "start_time": datetime.now()}

    async def start(self) -> dict:
        self.page = await self.session.get_auth_session()
        await self.page.goto(self.tax_debt_url, wait_until="domcontentloaded")
        date_received = await self.get_last_received_date()
        if datetime.now() - date_received > timedelta(days=self.time_delta):
            await self.request_to_kgd()
            date_received = datetime.now()
        await self.session.close_session()
        await self.set_result(date_received)
        return self.result

    async def get_last_received_date(self) -> datetime:
        tax_debt_html = await self.page.content()
        soup = BeautifulSoup(tax_debt_html, "html.parser")
        first_row = (
            soup.find("table", class_="table table-bordered").find("tbody").find("tr")
        )
        date_received_str = first_row.find_all("td")[3].text.strip()
        date_received = datetime.strptime(date_received_str, "%Y-%m-%d %H:%M:%S")
        return date_received

    async def request_to_kgd(self) -> None:
        button = await self.page.wait_for_selector("input[name='send_request']") 
        print('button: ', button)
        # await button.click()
        await self.page.wait_for_timeout(5000)

    async def set_result(self, date_received) -> None:
        self.result["finish_time"] = datetime.now()
        self.result["last_received_date"] = date_received
        logger.info(f"Finish {self.__class__.__name__}! Last received: {date_received}")
