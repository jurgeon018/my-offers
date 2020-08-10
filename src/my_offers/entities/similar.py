from dataclasses import dataclass
from typing import Optional

from my_offers import enums


@dataclass
class OfferSimilar:
    offer_id: int
    """Id объявления"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""
    group_id: Optional[int]
    """Id группы дублей"""
    district_id: Optional[int]
    """Id района"""
    house_id: Optional[int]
    """Id дома"""
    price: Optional[float]
    """Цена"""
    rooms_count: Optional[int]
    """Кол-во комнат"""
