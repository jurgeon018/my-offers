from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from my_offers import enums
from my_offers.entities.get_offers import PageInfo, Pagination
from my_offers.entities.offer_view_model import Underground


@dataclass
class GetOfferDuplicatesRequest:
    offer_id: int
    """Id объявления"""
    pagination: Optional[Pagination]
    """Параметры страницы"""
    type: Optional[enums.DuplicateTabType] = None
    """Вкладка дубликатов"""


@dataclass
class PriceInfo:
    exact: Optional[str]
    """Цена"""
    range: Optional[List[str]]
    """Диапазон цен"""
    trend: Optional[enums.PriceTrend]
    """Тенденция цены"""


@dataclass
class MobileUnderground:
    region_id: int
    """ID региона"""
    line_color: str
    """Цвет линии метро"""
    name: str
    """Название метро"""


@dataclass
class MobileOfferGeo:
    address: List[str]
    """Адрес"""
    underground: Optional[MobileUnderground]
    """Метро"""


@dataclass
class OfferDuplicate:
    offer_id: int
    """Id объявления"""
    deal_type: enums.DealType
    """Тип сделки"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""
    main_photo_url: Optional[str]
    """Основаная фотография объекта"""
    properties: List[str]
    """Свойства: комнаты, площадь и т.д."""
    geo: MobileOfferGeo
    """Гео"""
    display_date: Optional[datetime]
    """Дата для отображения в карточке"""
    price_info: PriceInfo
    """Инофрмация о цене"""
    vas: List[enums.OfferVas]
    """Список VAS'ов"""
    auction_bet: Optional[str]
    """Текущая ставка аукциона"""
    type: enums.DuplicateType
    """Тип дубликатов"""


@dataclass
class Tab:
    type: enums.DuplicateTabType
    """Тип вкладки"""
    title: str
    """Заголовок"""
    count: int
    """Кол-во"""


@dataclass
class GetOfferDuplicatesResponse:
    offers: List[OfferDuplicate]
    """Список объявлений"""
    tabs: List[Tab]
    """Информация о вкладках"""
    page: PageInfo
    """Информация о странице"""


@dataclass
class GetOffersDuplicatesCountRequest:
    offer_ids: List[int]
    """Id объявлений"""


@dataclass
class OfferDuplicatesCount:
    offer_id: int
    """Id объявления"""
    competitors_count: int
    """Кол-во похожих"""
    duplicates_count: int
    """Кол-во дублей"""


@dataclass
class GetOffersDuplicatesCountResponse:
    data: List[OfferDuplicatesCount]
