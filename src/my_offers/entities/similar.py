from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from my_offers import enums


@dataclass
class OfferSimilar:
    offer_id: int
    """Id объявления"""
    deal_type: enums.DealType
    """Тип сделки"""
    sort_date: datetime
    """Дата для сортировки"""
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
    old_price: Optional[float] = None
    """Старая цена"""
