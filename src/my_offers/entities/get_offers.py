from dataclasses import dataclass
from typing import List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import OfferViewModel


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
class GetOffer(OfferViewModel):
    statistics: Optional[Statistics] = None


@dataclass
class GetOffersResponse:
    offers: List[GetOffer]
    page: PageInfo
