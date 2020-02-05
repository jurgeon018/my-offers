from dataclasses import dataclass
from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi import entities as announcementapi_entities


@dataclass
class OfferViewModel:
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
