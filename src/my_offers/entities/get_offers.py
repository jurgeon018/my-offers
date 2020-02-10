from dataclasses import dataclass
from typing import List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import OfferViewModel
from my_offers.enums.sort_types import GetOffersSortType


@dataclass
class GetOffersRequest:
    status_tab: enums.GetOfferStatusTab
    """Вкладка"""
    sort_type: Optional[GetOffersSortType] = None
    """Тип сортировки"""
    deal_type: Optional[enums.DealType] = None
    """Тип сделки"""
    offer_type: Optional[enums.OfferType] = None
    """Тип объявления"""
    services: Optional[List[enums.Services]] = None
    """Тип размещения"""
    sub_agent_ids: Optional[List[int]] = None
    """Список сотрудников (только для мастрер аккаунтов)"""
    has_photo: Optional[bool] = None
    """Только с фото"""
    is_manual: Optional[bool] = None
    """Только ручные"""
    is_in_hidden_base: Optional[bool] = None
    """Только видимые агентам"""
    search_text: Optional[str] = None
    """Полнотекстовый поиск по объявлению"""


@dataclass
class Statistics:
    shows: Optional[int] = None
    """Количество показов в поиске"""
    views: Optional[int] = None
    """Количество просмотров карточки"""
    favorites: Optional[int] = None
    """Количество добавлений в избранное"""


@dataclass
class Auction:
    bet: Optional[int] = None
    """Текущая ставка аукциона"""
    district_place: Optional[int] = None
    """Позиция конкуренции по району"""
    home_place: Optional[int] = None
    """Позиция конкуренции по дому"""


@dataclass
class GetOffer(OfferViewModel):
    statistics: Optional[Statistics] = None
    """Статистика по объявлению"""
    auction: Optional[Auction] = None
    """Данные об аукционе по объявлению"""


@dataclass
class OfferCounters:
    active: int
    not_active: int
    declined: int
    archived: int


@dataclass
class GetOffersResponse:
    offers: List[GetOffer]
    counters: OfferCounters
