from dataclasses import dataclass
from typing import Dict, List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import OfferViewModel
from my_offers.enums.sort_types import GetOffersSortType
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


@dataclass
class Filter:
    status_tab: enums.GetOfferStatusTab
    """Вкладка"""
    sort_type: Optional[GetOffersSortType]
    """Тип сортировки"""
    deal_type: Optional[enums.DealType]
    """Тип сделки"""
    offer_type: Optional[enums.OfferType]
    """Тип объявления"""
    services: Optional[List[Services]]
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
class Pagination:
    page: Optional[int]
    """Номер страницы начиная с 1"""
    limit: Optional[int]
    """Количество объявлений на страницу"""
    offset: Optional[int]
    """Отступ от начала"""


@dataclass
class GetOffersRequest:
    filters: Filter
    """Параметры фильтрации"""
    pagination: Optional[Pagination]
    """Параметры страницы"""
    sort: Optional[enums.GetOffersSortType]
    """Сортировка"""


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
    active: Optional[int]
    not_active: Optional[int]
    declined: Optional[int]
    archived: Optional[int]


@dataclass
class PageInfo:
    count: int
    """Количество  объектов"""
    can_load_more: bool
    """Это не последняя страница"""
    page_count: int
    """Количество страниц"""


@dataclass
class GetOffersResponse:
    offers: List[GetOffer]
    counters: OfferCounters
    page: PageInfo
    degradation: Dict[str, bool]
