import re
from typing import List


class IinBinValidator:
    """Валидация iin и bin"""

    @classmethod
    def validate_bin(cls, _bin: str) -> bool:
        if re.search(r"^\d{12}$", _bin.strip(), re.IGNORECASE) is None:
            return False

        if _bin in cls.exclusion_bin:
            return True

        if int(_bin[4:5]) in (0, 1, 2, 3):
            return False

        if int(_bin[5:6]) not in (0, 1, 2, 3, 4):
            return False

        result = cls.calc_control_number(iin=_bin, weight=cls.__weight_1())
        if result == 10:
            result = cls.calc_control_number(iin=_bin, weight=cls.__weight_2())

        if result < 10:
            return result == int(_bin[11:12])
        else:
            return False

    @classmethod
    def validate_iin(cls, iin: str) -> bool:
        if re.search(r"^\d{12}$", iin.strip(), re.IGNORECASE) is None:
            return False

        if iin in cls.exclusion_iin:
            return True

        if int(iin[4:5]) not in (0, 1, 2, 3):
            return False

        if int(iin[6:7]) not in (1, 2, 3, 4, 5, 6):
            return False

        result = cls.calc_control_number(iin=iin, weight=cls.__weight_1())
        if result == 10:
            result = cls.calc_control_number(iin=iin, weight=cls.__weight_2())

        if result < 10:
            return result == int(iin[11:12])
        else:
            return False

    @staticmethod
    def __weight_1() -> List[int]:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    @staticmethod
    def __weight_2() -> List[int]:
        return [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]

    @staticmethod
    def calc_control_number(iin: str, weight: List[int]) -> int:
        i, result = 0, 0
        while i < len(iin) - 1:
            result = result + (weight[i] * int(iin[i]))
            i += 1
        return result % 11

    exclusion_bin = ("000003319944",)
    exclusion_iin = ("841006000754",)
