from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from .auth import GoszakupAuth


class TenderCancelManager:

    applications_url = "https://v3bl.goszakup.gov.kz/ru/myapp"

    def __init__(self, announce_number, auth_data, page: Page = None) -> None:
        self.announce_number = announce_number
        self.auth_data = auth_data
        self.page = page
        if not self.page:
            self.session = GoszakupAuth(auth_data)

    async def cancel(self) -> dict:
        if not self.page:
            self.page = await self.session.get_auth_session()
        await self.page.goto(self.applications_url, wait_until="domcontentloaded")
        await self.click_cancel_and_confirm_btn()
        return {"success": True, "message": "Tender canceled successfully"}

    async def click_cancel_and_confirm_btn(self) -> None:
        link = await self.page.wait_for_selector(f"a[href*='{self.announce_number}']")
        row = await link.evaluate_handle('element => element.closest("tr")')
        delete_button = await row.query_selector("a[onclick*='doDel']")
        await delete_button.click()
        modal_visible = await self.page.wait_for_selector(".modal.fade.in")
        if modal_visible:
            delete_button_in_modal = await modal_visible.wait_for_selector(
                "button[type='submit']"
            )
            await delete_button_in_modal.click()

    async def close_session(self) -> None:
        await self.session.close_session()
