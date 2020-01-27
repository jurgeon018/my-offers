from dataclasses import dataclass

from my_offers import enums


@dataclass
class Offer:
    offer_id: int
    """Id объявления"""
    master_user_id: int
    """Id мастер агента"""
    user_id: int
    """Id агента"""
    deal_type: enums.DealType
    """Тип сделки"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""
    search_text: str
    """Текст для поиска"""
    row_version: int
    """Версия записи"""
