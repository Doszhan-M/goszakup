from .scraper import Scraper


class E032Scraper(Scraper):
    """Scraper for egov e032."""

    _keywords_ru = {
        "Наименование": "comp_name_ru",
        "БИН": "iin_bin",
        "Регистрирующий орган": "reg_institution_ru",
        "Вид регистрации": "reg_type_ru",
        "Статус": "status_ru",
        "Дата последней (пере)регистрации": "last_rereg_date_ru",
        "Дата первичной регистрации": "first_reg_date_ru",
        "Головная организация": "parent_comp_ru",
        "Первый руководитель": "first_head_ru",
        "Количество участников (членов)": "heads_num",
        "Виды деятельности": "oked_ru",
        "Местонахождение": "location_ru",
    }
    _keywords_kz = {
        "Атауы": "comp_name_kz",
        "БСН": "iin_bin",
        "Тіркеуші орган": "reg_institution_kz",
        "Тіркеу түрі": "reg_type_kz",
        "Мәртебе": "status_kz",
        "Соңғы (қайта) тіркеу күні": "last_rereg_date_kz",
        "Алғашқы тіркеу күні": "first_reg_date_kz",
        "Бас ұйым": "parent_comp_kz",
        "Бірінші басшы": "first_head_kz",
        "Қатысушылардың саны (мүшесі)": "heads_num",
        "Қызмет түрі": "oked_kz",
        "Орналасқан жері": "location_kz",
    }

    def __init__(self, url, session, headers, iin_bin) -> None:
        super().__init__(url, session, headers, iin_bin)
        self.result = {}
        self._result_ru = {}
        self._result_kz = {}

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
            if text in self._keywords_ru.keys():
                self._result_ru[self._keywords_ru[text]] = self._spans_ru[counter + 1]
            elif text == "Учредители (участники, члены)":
                other_heads = self.collect_other_heads(
                    counter, "Количество участников (членов)", self._spans_ru
                )
                self.result["other_heads_ru"] = other_heads
            counter += 1
        return self._result_ru

    def gather_data_kz(self) -> dict:
        """Gather data from soup_ru."""

        counter = 0
        for text in self._spans_kz:
            text = text.strip()
            if text in self._keywords_kz.keys():
                self._result_kz[self._keywords_kz[text]] = self._spans_kz[counter + 1]
            elif text == "Құрылтайшылар (қатысушылар, бастамашы азаматтар)":
                other_heads = self.collect_other_heads(
                    counter, "Қатысушылардың саны (мүшесі)", self._spans_kz
                )
                self.result["other_heads_kz"] = other_heads
            counter += 1
        return self._result_kz
