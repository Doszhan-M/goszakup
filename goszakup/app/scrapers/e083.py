from .scraper import Scraper


class E083Scraper(Scraper):
    """Scraper for egov e083."""

    _keywords_ru = {
        "Наименование": "comp_name_ru",
        "БИН": "iin_bin",
        "Регистрирующий орган": "reg_org_ru",
        "Обременение на долю учредителя юридического лица:": "founder_encumbrance_ru",
        "Обременение на долю юридического лица, являющегося учредителем в других юридических лицах:": "legal_entity_encumbrance_ru",
    }
    _keywords_kz = {
        "Атауы": "comp_name_kz",
        "БСН": "iin_bin",
        "Тіркеуші орган": "reg_org_kz",
        "Заңды тұлға құрылтайшысының үлесіне ауыртпалық:": "founder_encumbrance_kz",
        "Басқа заңды тұлғаның үлесіне ауыртпалық:": "legal_entity_encumbrance_kz",
    }

    def __init__(self, url, session, headers, iin_bin) -> None:
        super().__init__(url, session, headers, iin_bin)
        self.result = {}
        self._result_ru = {"prohibition_ru": []}
        self._result_kz = {"prohibition_kz": []}

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
            elif text == "Запрет на регистрационное действие:":
                self._result_ru["prohibition_ru"].append(self._spans_ru[counter + 1])
            counter += 1
        return self._result_ru

    def gather_data_kz(self) -> dict:
        """Gather data from soup_ru."""

        counter = 0
        for text in self._spans_kz:
            text = text.strip()
            if text in self._keywords_kz.keys():
                self._result_kz[self._keywords_kz[text]] = self._spans_kz[counter + 1]
            elif text == "Тіркеу әрекетіне тыйым салу:":
                self._result_kz["prohibition_kz"].append(self._spans_kz[counter + 1])
            counter += 1
        return self._result_kz
