from .scraper import Scraper


class E080Scraper(Scraper):
    """Scraper for egov e080."""

    _keywords_ru = {
        "Наименование": "comp_name_ru",
        "Регистрирующий орган": "reg_institution_ru",
        "Дата последней перерегистрации": "last_rereg_date_ru",
        "Дата первичной регистрации": "first_reg_date_ru",
        "БИН": "iin_bin",
        "Руководитель": "first_head_ru",
        "Количество участников (членов)": "heads_num",
        "Вид деятельности": "oked_ru",
        "Местонахождение": "location_ru",
    }
    _keywords_kz = {
        "Атауы": "comp_name_kz",
        "Тіркеуші орган": "reg_institution_kz",
        "Соңғы (қайта) тіркеу күні": "last_rereg_date_kz",
        "Алғашқы тіркеу күні": "first_reg_date_kz",
        "БСН": "iin_bin",
        "Бірінші басшы": "first_head_kz",
        "Қатысушылардың саны(мүшесі)": "heads_num",
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

        data_ru = self.gather_data_ru()
        data_kz = self.gather_data_kz()
        self.result.update({**data_ru, **data_kz})
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
            if text == "Местонахождение":
                actions = self.collect_reg_actions(counter + 2, self._spans_ru)
                self._result_ru["reg_actions_ru"] = actions
                break
            counter += 1
        return self._result_ru

    def gather_data_kz(self) -> dict:
        """Gather data from soup_kz."""

        counter = 0
        for text in self._spans_kz:
            text = text.strip()
            if text in self._keywords_kz.keys():
                self._result_kz[self._keywords_kz[text]] = self._spans_kz[counter + 1]
            elif text == "Құрылтайшылар (қатысушылар, мүшелер)":
                other_heads = self.collect_other_heads(
                    counter, "Қатысушылардың саны(мүшесі)", self._spans_kz
                )
                self.result["other_heads_kz"] = other_heads
            if text == "Орналасқан жері":
                actions = self.collect_reg_actions(counter + 2, self._spans_kz)
                self._result_kz["reg_actions_kz"] = actions
                break
            counter += 1
        return self._result_kz

    def collect_reg_actions(self, counter, spans) -> list:
        """Collect registration actions."""

        actions = []
        i = counter
        while i < len(spans):
            try:
                action = {
                    "date": spans[i],
                    "action": spans[i + 1],
                }
                i += 2
            except IndexError:
                break
            actions.append(action)
        return actions
