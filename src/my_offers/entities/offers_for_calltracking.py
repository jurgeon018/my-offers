from dataclasses import dataclass
from typing import List, Optional

from my_offers.entities import MobileOfferGeo


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


@dataclass
class OffersForCalltrackingResponse:
    offers: List[OfferForCalltracking]


@dataclass
class OffersForCalltrackingCardResponse:
    offers: List[OfferForCalltrackingCard]
