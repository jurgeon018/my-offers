# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum

from .tariff_identificator import TariffIdentificator


class ExcludedServices(StrEnum):
    __value_format__ = NoFormat
    highlight = 'highlight'
    premium = 'premium'
    top3 = 'top3'


class Services(StrEnum):
    __value_format__ = NoFormat
    free = 'free'
    highlight = 'highlight'
    paid = 'paid'
    premium = 'premium'
    top3 = 'top3'
    calltracking = 'calltracking'
    auction = 'auction'


class Type(StrEnum):
    __value_format__ = NoFormat
    daily_limited = 'dailyLimited'
    """Ограниченная по дням публикация, подневная тарификация"""
    daily_termless = 'dailyTermless'
    """Бессрочная публикация, подневная тарификация"""
    periodical = 'periodical'
    """Тарификация за весь период"""


@dataclass
class PublishTerm:
    """Условия размещения"""

    days: Optional[int] = None
    """Количество дней"""
    dynamicPrice: Optional[float] = None
    """Стоимость услуги, которая может меняться пользователем"""
    excludedServices: Optional[List[ExcludedServices]] = None
    """Условия размещения, которые нельзя применять к объявлению"""
    ignoreServicePackages: Optional[bool] = None
    """Не использовать пакет размещений при публикации объявления"""
    services: Optional[List[Services]] = None
    """Список размещений"""
    tariffIdentificator: Optional[TariffIdentificator] = None
    """Идентификатор записи в тарифной сетке."""
    type: Optional[Type] = None
    """Тип тарификации"""
