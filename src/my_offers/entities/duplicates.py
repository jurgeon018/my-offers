from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers import enums
from my_offers.entities.get_offers import PageInfo, Pagination


@dataclass
class GetOfferDuplicatesRequest:
    offer_id: int
    """Id объявления"""
    pagination: Optional[Pagination]
    """Параметры страницы"""
    type: Optional[enums.DuplicateTabType] = None
    """Вкладка дубликатов"""


@dataclass
class GetOfferDuplicatesDesktopRequest:
    offer_id: int
    """Id объявления"""
    pagination: Optional[Pagination]
    """Параметры страницы"""


@dataclass
class GetOfferDuplicatesTabsRequest:
    offer_id: int
    """Id объявления"""


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
class OfferDuplicateDesktop:
    offer_id: int
    """Id объявления"""
    url: str
    """URL объявления"""
    title: str
    """Заголовок объявления"""
    geo: MobileOfferGeo
    """Гео"""
    price_info: PriceInfo
    """Инофрмация о цене"""
    vas: List[enums.OfferVas]
    """Список VAS'ов"""
    type: enums.DuplicateType
    """Тип дубликатов"""
    display_date: Optional[datetime] = None
    """Дата для отображения в карточке"""
    auction_bet: Optional[str] = None
    """Текущая ставка аукциона"""
    main_photo_url: Optional[str] = None
    """Основаная фотография объекта"""


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
class DuplicateSubscription:
    subscribed_on_duplicate: bool
    """Подписан ли пользователь на дубли по своим объявлениям"""
    email: Optional[str] = None
    """Email пользователя (только если есть активная подписка)"""


@dataclass
class GetOfferDuplicatesDesktopResponse:
    offers: List[OfferDuplicateDesktop]
    """Список объявлений"""
    page: PageInfo
    """Информация о странице"""
    subscription: DuplicateSubscription
    """Информация о подписке на дубликаты объявлений"""


@dataclass
class GetOfferDuplicatesTabsResponse:
    tabs: List[Tab]
    """Информация о вкладках"""


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


@dataclass
class OfferSimilarCounter:
    offer_id: int
    """Id объявления"""
    total_count: int
    """Общее кол-во"""
    same_building_count: int
    """Кол-во в этом доме"""
    similar_count: int
    """Кол-во похожих"""
    duplicates_count: int
    """Кол-во дублей"""
