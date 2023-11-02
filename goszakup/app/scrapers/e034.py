from .scraper import Scraper


class E034Scraper(Scraper):
    """Scraper for egov e034."""

    _keywords_ru = {
        "Наименование юридического лица": "comp_name_ru",
        "БИН": "iin_bin",
        "Регистрирующий орган": "reg_institution_ru",
        "Дата последней перерегистрации": "last_rereg_date_ru",
        "Дата первичной регистрации": "first_reg_date_ru",
        "Руководитель": "first_head_ru",
        "Количество участников (членов)": "heads_num",
        "Местонахождение": "location_ru",
    }
    _keywords_kz = {
        "Атауы": "comp_name_kz",
        "БСН": "iin_bin",
        "Тіркеуші орган": "reg_institution_kz",
        "Соңғы қайта тіркеу күні": "last_rereg_date_kz",
        "Алғашқы тіркеу күні": "first_reg_date_kz",
        "Бірінші басшы": "first_head_kz",
        "Қатысушылардың саны(мүшесі": "heads_num",
        "Орналасқан жері": "location_kz",
    }

    def __init__(self, url, session, headers, iin_bin) -> None:
        super().__init__(url, session, headers, iin_bin)
        self.result = {}
        self._result_ru = {"involvement_in_other_companies_ru": []}
        self._result_kz = {"involvement_in_other_companies_kz": []}

    def gather_data(self) -> dict:
        """Gather data from soup objects."""

        self.gather_data_ru()
        self.gather_data_kz()
        self.result.update({**self._result_ru, **self._result_kz})
        return self.result

    def gather_data_ru(self) -> dict:
        """Gather data from soup_ru."""

        counter = 0
        flag = True
        for text in self._spans_ru:
            text = text.strip()
            if text in self._keywords_ru.keys() and flag:
                self._result_ru[self._keywords_ru[text]] = self._spans_ru[counter + 1]
            elif text == "Учредители (участники, члены)":
                other_heads = self.collect_other_heads(
                    counter, "Количество участников (членов)", self._spans_ru
                )
                self.result["other_heads_ru"] = other_heads
            elif text == "Участие юридического лица в других юридических лицах:":
                flag = False
                blocks = self.gather_company_blocks(counter + 2, self._spans_ru)
                self._result_ru["involvement_in_other_companies_ru"] = blocks
            counter += 1
        return self._result_ru

    def gather_data_kz(self) -> dict:
        """Gather data from soup_kz."""

        counter = 0
        flag = True
        for text in self._spans_kz:
            text = text.strip()
            if text in self._keywords_kz.keys() and flag:
                self._result_kz[self._keywords_kz[text]] = self._spans_kz[counter + 1]
            elif text == "Құрылтайшылар (қатысушылар, мүшелер)":
                other_heads = self.collect_other_heads(
                    counter, "Қатысушылардың саны(мүшесі)", self._spans_kz
                )
                self.result["other_heads_kz"] = other_heads
            elif text == "Заңды тұлғаның өзге заңды тұлғаға қатысуы:":
                flag = False
                blocks = self.gather_company_blocks(counter + 2, self._spans_kz)
                self._result_kz["involvement_in_other_companies_kz"] = blocks
            counter += 1
        return self._result_kz

    def gather_company_blocks(self, counter, spans) -> list:
        blocks = []
        while counter < len(spans):
            try:
                company = {
                    "name": spans[counter],
                    "bin": spans[counter + 2],
                    "reg_organization": spans[counter + 4],
                    "first_reg_date": spans[counter + 6],
                    "head": spans[counter + 8],
                    "okeds": spans[counter + 10],
                    "location": spans[counter + 12],
                }
                counter += 14
            except IndexError:
                break
            blocks.append(company)
        return blocks
