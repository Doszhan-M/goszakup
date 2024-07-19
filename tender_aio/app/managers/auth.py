import aiohttp
import json
import grpc
import asyncio
from uuid import uuid4
from logging import getLogger
from playwright.async_api import Page
from playwright.async_api import async_playwright

from app.pb2 import eds_pb2
from app.pb2 import eds_pb2_grpc
from app.services import get_aiohttp_session, AiohttpSession


logger = getLogger("fastapi")
active_sessions = {}


class GoszakupAuth:
    """Manager for getting cookie from goszakup.gov.kz."""

    def __init__(self, auth_data, *args, **kwargs):
        self.auth_url = "https://v3bl.goszakup.gov.kz/ru/user/"
        self.key_url = "https://v3bl.goszakup.gov.kz/ru/user/sendkey/kz"
        self.goszakup_pass = auth_data.goszakup_pass
        self.ssid = uuid4()
        self.session_manager = AiohttpSession()
        self.session: aiohttp.ClientSession = None
        self.auth_data = auth_data
        self.headers = {
            "Host": "v3bl.goszakup.gov.kz",
            "Content-Length": "0",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Origin": "https://v3bl.goszakup.gov.kz",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://v3bl.goszakup.gov.kz/ru/user/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
            "Connection": "keep-alive",
        }

    async def print_cookies(self):
        if self.session:
            for cookie in self.session.cookie_jar:
                print(f"{cookie.key}: {cookie.value}")
                
    async def get_auth_session(self) -> Page:
        self.session = await self.session_manager.start()
        await self.session.get(self.auth_url,)
        response = await self.session.post(
            self.key_url, 
        )
        await self.print_cookies()
        key = await response.text()
        signed_xml = await self.wakeup_nclayer_and_get_signed_xml(key)
        url = "https://v3bl.goszakup.gov.kz/user/sendsign/kz"
        headers = {
            "Host": "v3bl.goszakup.gov.kz",
            "Content-Length": str(len(signed_xml)),
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Accept-Language": "en-US",
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Origin": "https://v3bl.goszakup.gov.kz",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://v3bl.goszakup.gov.kz/ru/user/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
            "Connection": "keep-alive",
        }
        await self.session.post(url, data=signed_xml)
        url = "https://v3bl.goszakup.gov.kz/ru/user/auth_confirm"
        headers = {
            "Host": "v3bl.goszakup.gov.kz",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Accept-Language": "en-US",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://v3bl.goszakup.gov.kz/ru/user/",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i",
            "Connection": "keep-alive",
        }
        response = await self.session.get(url)
        html = await response.text()
        self.save_html(html)

        # self.save_html(html)
        # nclayer_call_btn = await self.page.query_selector("#selectP12File")
        # async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
        #     stub = eds_pb2_grpc.EdsServiceStub(channel)
        #     eds_manager_status = stub.SendStatus(eds_pb2.EdsManagerStatusCheck())
        #     async for status in eds_manager_status:
        #         if status.busy.value:
        #             logger.info("Eds Service is busy. Waiting...")
        #     await nclayer_call_btn.click()
        #     eds_data = eds_pb2.SignByEdsStart(
        #         eds_path=self.auth_data.eds_gos,
        #         eds_pass=self.auth_data.eds_pass,
        #     )
        #     sign_by_eds = await stub.ExecuteSignByEds(eds_data)
        #     if sign_by_eds.result:
        #         await self.enter_goszakup_password()
        # await self.store_auth_session()
        return self.session

    async def wakeup_nclayer_and_get_signed_xml(self, key):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # Запуск браузера
            page = await browser.new_page()
            await page.goto("http://127.0.0.1:9000")
            xml_data = (
                f'<?xml version="1.0" encoding="UTF-8"?><root><key>{key}</key></root>'
            )
            last_message = await page.evaluate_handle(
                f"""
                (async () => {{
                    const url = "wss://127.0.0.1:13579/";
                    const initialPayload = {{
                        "module": "NURSign",
                        "type": "version"
                    }};
                    const subsequentPayload = {{
                        "module": "NURSign",
                        "type": "xml",
                        "data": `{xml_data}`,
                        "source": "local"
                    }};
                    return new Promise((resolve, reject) => {{
                        const websocket = new WebSocket(url);
                        websocket.onopen = function(event) {{
                            console.log("Connection opened");
                            websocket.onmessage = function(event) {{
                                console.log("Initial Received: ", event.data);
                                websocket.send(JSON.stringify(initialPayload));
                                websocket.onmessage = function(event) {{
                                    console.log("Received: ", event.data);
                                    websocket.send(JSON.stringify(subsequentPayload));
                                    websocket.onmessage = function(event) {{
                                        console.log("Received: ", event.data);
                                        resolve(event.data);
                                    }};
                                }};
                            }};
                        }};
                        websocket.onerror = function(event) {{
                            console.error("WebSocket error: ", event);
                            reject(event);
                        }};
                        websocket.onclose = function(event) {{
                            console.log("Connection closed: ", event);
                        }};
                    }});
                }})()
            """
            )
            message = json.loads(await last_message.json_value())["result"]
            await browser.close()
            return message

    def save_html(self, html: str) -> None:
        """Сохранить спарсенный блок в html файл."""

        with open("./app/test.html", "w") as file:
            file.write(html)

    async def enter_goszakup_password(self):
        password_field = await self.page.wait_for_selector(
            "input[name='password']", timeout=5000
        )
        await password_field.fill(self.goszakup_pass)
        checkbox = await self.page.query_selector("#agreed_check")
        if not await checkbox.is_checked():
            await checkbox.click()
        login_button = await self.page.query_selector(".btn-success")
        await login_button.click()

    async def store_auth_session(self):
        global active_sessions
        active_sessions[self.ssid] = {"page": self.page}
        logger.info(f"Store new session id: {self.ssid}")

    async def close_session(self):
        if self.ssid in active_sessions:
            session = active_sessions[self.ssid]
            await session["page"].close()
            del active_sessions[self.ssid]
            logger.info(f"Closed and removed session id: {self.ssid}")
