from re import search

from .scraper import Scraper


class E035Scraper(Scraper):
    """Scraper for egov e035."""

    def __init__(self, url, session, headers, iin_bin) -> None:
        super().__init__(url, session, headers, iin_bin)
        self.result = {"iin_bin": self.iin_bin}
        self._result_ru = {"other_comps_ru": []}
        self._result_kz = {"other_comps_kz": []}

    def gather_data(self) -> dict:
        """Gather data from soup objects."""

        self.gather_data_ru()
        self.gather_data_kz()
        self.result.update({**self._result_ru, **self._result_kz})
        return self.result

    def gather_data_ru(self) -> dict:
        """Gather data from soup_ru."""

        counter = 0
        for text in self._spans_ru:
            text = text.strip()
            if text == "Ф.И.О.":
                self._result_ru["fio"] = self._spans_ru[counter + 1]
            elif text == "Участие физического лица в других юридических лицах:":
                if search("не участвует", self._spans_ru[counter + 1]):
                    self._result_ru["is_in_other_comp"] = False
                else:
                    self._result_ru["is_in_other_comp"] = True
                    blocks = self.gather_company_blocks(counter + 2, self._spans_ru)
                    self._result_ru["other_comps_ru"] = blocks
            counter += 1
        return self._result_ru

    def gather_data_kz(self) -> dict:
        """Gather data from soup_kz."""

        counter = 0
        for text in self._spans_kz:
            text = text.strip()
            if text == "Т.А.Ж.":
                self._result_kz["fio"] = self._spans_kz[counter + 1]
            elif text == "Жеке тұлғаның басқа заңды тұлғаларға қатысуы:":
                if search("қатыспайды", self._spans_kz[counter + 1]):
                    self._result_kz["is_in_other_comp"] = False
                else:
                    self._result_kz["is_in_other_comp"] = True
                    blocks = self.gather_company_blocks(counter + 2, self._spans_kz)
                    self._result_kz["other_comps_kz"] = blocks
            counter += 1
        return self._result_kz

    def gather_company_blocks(self, counter, spans) -> list:
        """Collect companies as object in list"""

        blocks = []
        while counter < len(spans):
            try:
                company = {
                    "name": spans[counter],
                    "bin": spans[counter + 2],
                    "reg_organization": spans[counter + 4],
                    "last_rereg_date": spans[counter + 6],
                    "first_reg_date": spans[counter + 8],
                    "head": spans[counter + 10],
                    "location": spans[counter + 12],
                }
                counter += 14
            except IndexError:
                break
            blocks.append(company)
        return blocks
