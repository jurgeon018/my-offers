from dataclasses import dataclass
from typing import List, Optional

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi import entities as announcementapi_entities


@dataclass
class GetOffersRequest:
    user_id: int
    status_tab: enums.GetOfferStatusTab
    """Статус (Вкладка)"""
    deal_type: Optional[enums.DealType] = None
    offer_type: Optional[enums.GetOfferType] = None
    sub_agent_ids: Optional[List[int]] = None
    has_photo: Optional[bool] = None
    is_manual: Optional[bool] = None
    is_in_hidden_base: Optional[bool] = None
    search_text: Optional[str] = None
    services: Optional[List[enums.Services]] = None


@dataclass
class PageInfo:
    count: int
    """Количество  объектов"""
    can_load_more: bool
    """Это не последняя страница"""


@dataclass
class Statistics:
    offer_show: int
    """просмотров объявления"""
    search_results_show: int
    """увидели в поиске"""
    favorites: int
    """добавили в избранное"""


@dataclass
class GetOffer:
    offer_id: int
    """Id объявления"""
    master_user_id: int
    """Id мастер агента"""
    user_id: int
    """Id агента"""
    bargain_terms: announcementapi_entities.BargainTerms
    """Условия сделки"""
    main_photo_url: Optional[str] = None
    """Основаная фотография объекта"""
    geo: Optional[announcementapi_entities.Geo] = None
    """Gets or Sets Geo"""
    building: Optional[announcementapi_entities.Building] = None
    """Информация о здании"""
    floor_number: Optional[int] = None
    """Этаж"""
    statistics: Optional[Statistics] = None


@dataclass
class GetOffersResponse:
    offers: List[GetOffer]
    page: PageInfo
