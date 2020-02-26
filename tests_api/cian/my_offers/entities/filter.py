# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client my-offers`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum


class DealType(StrEnum):
    __value_format__ = NoFormat
    rent = 'rent'
    """Аренда"""
    sale = 'sale'
    """Продажа"""


class OfferType(StrEnum):
    __value_format__ = NoFormat
    commercial = 'commercial'
    """Коммерческая"""
    flat = 'flat'
    """Жилая"""
    newobject = 'newobject'
    """Новостройки"""
    suburban = 'suburban'
    """Загородная"""


class Services(StrEnum):
    __value_format__ = NoFormat
    auction = 'auction'
    calltracking = 'calltracking'
    free = 'free'
    highlight = 'highlight'
    paid = 'paid'
    premium = 'premium'
    top3 = 'top3'


class SortType(StrEnum):
    __value_format__ = NoFormat
    by_area_max = 'byAreaMax'
    """По площади: возрастающая"""
    by_area_min = 'byAreaMin'
    """По площади: убывающая"""
    by_default = 'byDefault'
    """По-умолчанию"""
    by_offer_id = 'byOfferId'
    """По ID объявления"""
    by_price_for_meter = 'byPriceForMeter'
    """По цене за метр"""
    by_price_max = 'byPriceMax'
    """По цене: возрастающая"""
    by_price_min = 'byPriceMin'
    """По цене: убывающая"""
    by_street = 'byStreet'
    """По улице"""
    by_walk_time = 'byWalkTime'
    """По времени до метро"""


class StatusTab(StrEnum):
    __value_format__ = NoFormat
    active = 'active'
    """Активные"""
    archived = 'archived'
    """Архив"""
    declined = 'declined'
    """Отклоненные"""
    not_active = 'notActive'
    """Неактивные"""


@dataclass
class Filter:
    statusTab: StatusTab
    """Вкладка"""
    dealType: Optional[DealType] = None
    """Тип сделки"""
    hasPhoto: Optional[bool] = None
    """Только с фото"""
    isInHiddenBase: Optional[bool] = None
    """Только видимые агентам"""
    isManual: Optional[bool] = None
    """Только ручные"""
    offerType: Optional[OfferType] = None
    """Тип объявления"""
    searchText: Optional[str] = None
    """Полнотекстовый поиск по объявлению"""
    services: Optional[List[Services]] = None
    """Тип размещения"""
    sortType: Optional[SortType] = None
    """Тип сортировки"""
    subAgentIds: Optional[List[int]] = None
    """Список сотрудников (только для мастрер аккаунтов)"""
