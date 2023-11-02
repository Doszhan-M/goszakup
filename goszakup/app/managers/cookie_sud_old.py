import time
import requests
import asyncio
import aiohttp
from logging import getLogger
from bs4 import BeautifulSoup

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from .base import EgovBase
from app.services import get_web_driver
from app.services import aioredis, redis


logger = getLogger("fastapi")


class SudCookieParser(EgovBase):
    """Manager for getting cookie from sud.kz."""

    def __init__(self, *args, **kwargs):
        super(EgovBase, self).__init__(*args, **kwargs)
        self.session = requests.Session()

    _login_url: str = "https://office.sud.kz/loginByEDS.xhtml"

    async def reload_cookie(self) -> str:
        """Login sud.kz, get cookie, save cookie to redis"""

        raw_cookie = await asyncio.to_thread(self.login_sud1)
        return raw_cookie

    def login_sud1(self) -> list:
        """Log i to sud via eds and return cookie."""

        response = self.session.get(self._login_url)
        soup = BeautifulSoup(response.text, "lxml")
        view_state = soup.find(id="javax.faces.ViewState")["value"]
        xml_to_sign = soup.find(id="xmlToSign0")["value"]
        signed_data = self.sign_xml(xml_to_sign, self._eds_auth)
        signed_response = self.send_signed_eds_req(signed_data, view_state)
        cookies = self.session.cookies
        session_cookie = cookies.get("JSESSIONID")
        with open("1.html", "w") as file:
            file.write(signed_response.text)
        return session_cookie

    def send_signed_eds_req(self, signed_data, view_state) -> any:
        data = {
            "j_idt34": "j_idt34",
            "j_idt34:signedXml": signed_data,
            "j_idt34:j_idt42": "",
            "javax.faces.ViewState": view_state,
            "javax.faces.source": "j_idt34:j_idt52",
            "javax.faces.partial.execute": "j_idt34:j_idt52 @component",
            "javax.faces.partial.render": "@component",
            "org.richfaces.ajax.component": "j_idt34:j_idt52",
            "j_idt34:j_idt52": "j_idt34:j_idt52",
            "rfExt": "null",
            "AJAX:EVENTS_COUNT": "1",
            "javax.faces.partial.ajax": "true",
        }
        url = "https://office.sud.kz/loginByEDS.xhtml"
        response = self.session.post(url, data=data)
        return response

    def sign_xml(self, xml, eds) -> str:
        """Sign xml from egov by local ncanode"""

        payload = self.prepare_payload_for_sign(xml, eds)
        response = self.sync_post_request(self._ncanode_url, payload)
        signed_data = self.clear_signed_data(response)
        return signed_data

    def prepare_payload_for_sign(self, xml, eds) -> dict:
        """Prepare payload for sign by ncanode."""
        import re

        xml = re.sub("<\?xml[^>]+>", "", xml)
        payload = {
            "version": "1.0",
            "method": "XML.sign",
            "params": {
                "checkCrl": "false",
                "checkOcsp": "false",
                "p12": eds,
                "password": self._eds_pass,
                "xml": xml,
                "createTsp": False,
                "verifyOcsp": "false",
                "verifyCrl": "false",
                "useTsaPolicy": "TSA_GOST_POLICY",
            },
        }
        return payload

    def login_sud(self) -> list:
        """Log in to sud via eds and return cookie."""

        web_driver = get_web_driver()
        driver: Chrome = next(web_driver)
        driver.get(self._login_url)
        view_state = driver.find_element(By.ID, "javax.faces.ViewState").get_attribute(
            "value"
        )
        print("view_state: ", view_state)
        xml_to_sign = driver.find_element(By.ID, "xmlToSign0").get_attribute("value")
        print("xml_to_sign: ", xml_to_sign)
        signed_data = self.sign_xml(xml_to_sign, self._eds_auth)
        print("signed_data: ", signed_data)
        selenium_cookies = driver.get_cookies()
        signed_response = self.send_signed_eds(
            signed_data, view_state, selenium_cookies
        )
        with open("1.html", "w") as file:
            file.write(signed_response.text)
            print("signed_response.text: ", signed_response.text)
        driver.get("https://office.sud.kz/form/proceedings/services.xhtml")
        raw_cookie = driver.get_cookies()
        print("raw_cookie: ", raw_cookie)
        cookies = signed_response.cookies
        print("cookies: ", cookies)
        time.sleep(15)
        return raw_cookie

    def send_signed_eds(self, signed_data, view_state, selenium_cookies) -> any:
        session = requests.Session()
        for cookie in selenium_cookies:
            session.cookies.set(cookie["name"], cookie["value"])
        data = {
            "j_idt34": "j_idt34",
            "j_idt34:signedXml": signed_data,
            "j_idt34:j_idt42": "",
            "javax.faces.ViewState": view_state,
            "javax.faces.source": "j_idt34:j_idt52",
            "javax.faces.partial.execute": "j_idt34:j_idt52 @component",
            "javax.faces.partial.render": "@component",
            "org.richfaces.ajax.component": "j_idt34:j_idt52",
            "j_idt34:j_idt52": "j_idt34:j_idt52",
            "rfExt": "null",
            "AJAX:EVENTS_COUNT": "1",
            "javax.faces.partial.ajax": "true",
        }
        url = "https://office.sud.kz/loginByEDS.xhtml"
        response = session.post(url, data=data)
        return response


# TODO:  https://office.sud.kz/proxy/%D0%90%D0%9E+%C2%AB%D0%9A%D0%B0%D0%B7%D0%BF%D0%BE%D1%87%D1%82%D0%B0%C2%BB+%D0%BA+%D0%98%D0%9F+%C2%AB%D0%9A%D0%B8%D0%BC+%D0%9E.%D0%92.%C2%BB.pdf?t=1698683531487