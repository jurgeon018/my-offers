from dataclasses import dataclass
from typing import List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import OfferViewModel
from my_offers.enums.sort_types import GetOffersSortType


@dataclass
class GetOffersRequest:
    status_tab: enums.GetOfferStatusTab
    """Вкладка"""
    sort_type: Optional[GetOffersSortType]
    """Тип сортировки"""
    deal_type: Optional[enums.DealType]
    """Тип сделки"""
    offer_type: Optional[enums.OfferType]
    """Тип объявления"""
    services: Optional[List[enums.Services]]
    """Тип размещения"""
    sub_agent_ids: Optional[List[int]]
    """Список сотрудников (только для мастрер аккаунтов)"""
    has_photo: Optional[bool]
    """Только с фото"""
    is_manual: Optional[bool]
    """Только ручные"""
    is_in_hidden_base: Optional[bool]
    """Только видимые агентам"""
    search_text: Optional[str]
    """Полнотекстовый поиск по объявлению"""


@dataclass
class GetOffersPrivateRequest(GetOffersRequest):
    user_id: int
    """ID пользователя"""


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
    statistics: Optional[Statistics]
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
class PageInfo:
    count: int
    """Количество  объектов"""
    can_load_more: bool
    """Это не последняя страница"""


@dataclass
class GetOffersResponse:
    offers: List[GetOffer]
    counters: OfferCounters
    page: Optional[PageInfo] = None
