from dataclasses import dataclass
from typing import List, Optional

from my_offers import enums
from my_offers.entities import MobileOfferGeo
from my_offers.entities.offer_view_model import PriceInfo


@dataclass
class OffersForCalltrackingRequest:
    offer_ids: List[int]
    """Id объявлений"""


@dataclass
class OfferForCalltracking:
    offer_id: int
    """Id объявления"""
    main_photo_url: Optional[str]
    """Основаная фотография объекта"""


@dataclass
class OfferForCalltrackingCard:
    offer_id: int
    """Id объявления"""
    main_photo_url: Optional[str]
    """Основаная фотография объекта"""
    properties: List[str]
    """Свойства: комнаты, площадь и т.д."""
    geo: MobileOfferGeo
    """Гео"""
    deal_type: enums.DealType
    """Тип сделки"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""
    price_info: PriceInfo
    """Инофрмация о цене"""


@dataclass
class OffersForCalltrackingResponse:
    offers: List[OfferForCalltracking]


@dataclass
class OffersForCalltrackingCardResponse:
    offers: List[OfferForCalltrackingCard]
