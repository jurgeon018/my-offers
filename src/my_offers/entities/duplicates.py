from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from my_offers import enums
from my_offers.entities.get_offers import PageInfo, Pagination
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo


@dataclass
class GetOfferDuplicatesRequest:
    offer_id: int
    """Id объявления"""
    type: Optional[enums.DuplicateType]
    """Тип дубликатов"""
    pagination: Optional[Pagination]
    """Параметры страницы"""


@dataclass
class OfferDuplicate:
    offer_id: int
    """Id объявления"""
    main_photo_url: Optional[str]
    """Основаная фотография объекта"""
    properties: List[str]
    """Свойства: комнаты, площадь и т.д."""
    geo: OfferGeo
    """Гео"""
    display_date: Optional[datetime]
    """Дата для отображения в карточке"""
    price_info: PriceInfo
    """Инофрмация о цене"""
    vas: List[enums.OfferVas]
    """Список VAS'ов"""
    auction_bet: Optional[int]
    """Текущая ставка аукциона"""
    type: enums.DuplicateType
    """Тип дубликатов"""


@dataclass
class Counters:
    total: int
    """Общее количество"""
    duplicates: int
    """Кол-во дубликатов"""


@dataclass
class GetOfferDuplicatesResponse:
    offers: List[OfferDuplicate]
    """Список объявлений"""
    counters: Counters
    """Счеткики количества объявлений"""
    page: PageInfo
    """Информация о странице"""
    degradation: Dict[str, bool]
    """Информация о деградации"""
