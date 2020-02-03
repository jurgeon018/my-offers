from dataclasses import dataclass
from typing import Dict, List

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
    status_tab: enums.OfferStatusTab
    """Статус (Вкладка)"""
    search_text: str
    """Текст для поиска"""
    row_version: int
    """Версия записи"""
    services: List[enums.Services]
    """Список размещений"""
    raw_data: Dict
    """Модель объявления"""
    is_manual: bool
    """Подано в ручную"""
    is_in_hidden_base: bool
    """Объявление закрытой базы"""
    has_photo: bool
    """С фотографиями"""
