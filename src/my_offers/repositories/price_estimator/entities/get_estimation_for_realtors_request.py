# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client price-estimator`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import IntEnum, NoFormat, StrEnum
from cian_schemas import allow_for_api

from .estimation_user_chosen_filters import EstimationUserChosenFilters


class DealType(StrEnum):
    __value_format__ = NoFormat
    rent = 'rent'
    """Аренда"""
    sale = 'sale'
    """Продажа"""


@allow_for_api
class RoomsCount(IntEnum):
    value_0 = 0
    """Комната"""
    value_1 = 1
    """Однокомнатная квартира"""
    value_2 = 2
    """Двухкомнатная квартира"""
    value_3 = 3
    """Трехкомнатная квартира"""
    value_4 = 4
    """Четырехкомнатная квартира"""
    value_5 = 5
    """Пятикомнатная квартира"""
    value_6 = 6
    """Многокомнатная квартира (6 и более комнат)"""
    value_7 = 7
    """Квартира со свободной планировкой"""
    value_8 = 8
    """Доля квартиры"""
    value_9 = 9
    """Студия"""
    value_10 = 10
    """Койко-место"""


@dataclass
class GetEstimationForRealtorsRequest:
    address: str
    """Адрес дома"""
    area: float
    """Площадь"""
    deal_type: DealType
    """Тип сделки"""
    house_id: int
    """Id дома"""
    offer_id: int
    """ID объявления"""
    price: int
    """Цена квартиры в рублях"""
    rooms_count: RoomsCount
    """Кол-во комнат"""
    filters: Optional[List[EstimationUserChosenFilters]] = None
    """Выбранные пользователем фильтры"""