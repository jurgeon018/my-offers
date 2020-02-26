# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Currency(StrEnum):
    __value_format__ = NoFormat
    eur = 'eur'
    """Евро"""
    rur = 'rur'
    """Рубль"""
    usd = 'usd'
    """Доллар"""


@dataclass
class MonthlyIncome:
    """Прибыль"""

    currency: Optional[Currency] = None
    """Валюта"""
    income: Optional[float] = None
    """Прибыль"""
