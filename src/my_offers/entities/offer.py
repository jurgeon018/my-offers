from dataclasses import dataclass
from datetime import datetime

from typing import Dict, List, Optional

from my_offers import enums


@dataclass
class Offer:
    offer_id: int
    """Id объявления"""
    master_user_id: int
    """Id мастер агента"""
    # поля для фильтров
    user_id: int
    """Id агента"""
    status_tab: enums.OfferStatusTab
    """Статус (Вкладка)"""
    deal_type: enums.DealType
    """Тип сделки"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""
    services: List[enums.Services]
    """Список размещений"""
    is_manual: bool
    """Подано в ручную"""
    is_in_hidden_base: bool
    """Объявление закрытой базы"""
    has_photo: bool
    """С фотографиями"""
    # поля для поиска
    search_text: str
    """Текст для поиска"""
    # системные поля
    raw_data: Dict
    """Модель объявления"""
    row_version: int
    """Версия записи"""
    is_test: bool
    """Тестовое объявление"""
    # поля для сортировок
    price: Optional[float] = None
    """Цена"""
    price_per_meter: Optional[float] = None
    """Цена за квадратный метр"""
    total_area: Optional[float] = None
    """Общая площадь, м²"""
    street_name: Optional[str] = None
    """Название улицы"""
    walking_time: Optional[int] = None
    """Время в пути в минутах до метро пешком, мин"""
    sort_date: Optional[datetime] = None
    """Дата для сортировки"""
