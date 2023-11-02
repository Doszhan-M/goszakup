from os import path
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from aiohttp.client import ClientSession


class Scraper(ABC):
    """Main class with common parameters for scraper descendants."""

    def __init__(self, urls, session, headers, iin_bin=None) -> None:
        self._session: ClientSession = session
        self._headers: dict = headers
        self.iin_bin = iin_bin
        self.urls: dict = urls.copy()
        self._soups: dict = urls
        self._soup_ru: BeautifulSoup = None
        self._soup_kz: BeautifulSoup = None
        self._spans_ru = []
        self._spans_kz = []

    async def scraping_pages(self):
        """Scraping pages from urls."""

        declined = self.is_declined()
        if not declined:
            await self.request_pages()
            self.collect_spans()
            result = self.gather_data()
            result["document_url_ru"] = self.urls["ru"]
            result["document_url_kz"] = self.urls["kz"]
        else:
            result = {
                "iin_bin": self.iin_bin,
                "decline_reason_ru": self._soups["statusGo"]["name"]["ru"],
                "decline_reason_kz": self._soups["statusGo"]["name"]["kk"],
            }
        return result

    def is_declined(self):
        """Scraping pages from urls."""

        declined_signs = self._soups.get("statusGo")
        if declined_signs:
            declined = True
        else:
            declined = False
        return declined

    async def request_pages(self) -> None:
        """Request html from urls."""

        for prefix, url in self._soups.items():
            async with self._session.get(url, headers=self._headers) as response:
                html = await response.text()
                # self.save_html(html, prefix)
                soup = BeautifulSoup(html, "html.parser")
                self._soups[prefix] = soup
        self._soup_ru = self._soups["ru"]
        self._soup_kz = self._soups["kz"]

    def collect_spans(self) -> None:
        """Collect all spans from soaps."""

        for spans in self._soup_ru.find_all("span"):
            self._spans_ru.append(spans.get_text("\n"))
        for i in self._soup_kz.find_all("span"):
            self._spans_kz.append(i.get_text("\n"))

    @abstractmethod
    def gather_data(self) -> dict:
        """Gather data from soup object."""
        pass

    def collect_other_heads(self, counter, stop_word, spans) -> list:
        """Collect other heads."""

        i = counter + 1
        other_heads = []
        while True:
            if spans[i].strip() == stop_word:
                break
            other_heads.append(spans[i].strip())
            i += 1
        return other_heads

    def save_html(self, data: str, prefix: str) -> None:
        """Save parsed block to html file."""

        dir_path = path.dirname(path.realpath(__file__))
        with open(f"{dir_path}_{prefix}.html", "w") as file:
            file.write(data)
