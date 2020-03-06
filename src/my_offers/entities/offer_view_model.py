from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers.enums.offer_address import AddressType


@dataclass
class PriceInfo:
    exact: Optional[str] = None
    """Цена"""
    range: Optional[List[str]] = None
    """Диапазон цен"""


@dataclass
class Subagent:
    id: int
    """ID агента"""
    name: str
    """Полное имя агнета"""


@dataclass
class Newbuilding:
    name: str
    """Название ЖК"""
    search_url: str
    """Поисковый запрос по ЖК"""


@dataclass
class Underground:
    region_id: int
    """ID региона"""
    line_color: str
    """Цвет линии метро"""
    name: str
    """Название метро"""
    search_url: str
    """Поисковый запрос по метро"""


@dataclass
class Address:
    name: str
    """Полный адрес"""
    search_url: str
    """Поисковый запрос по адресу"""
    type: AddressType


@dataclass
class OfferGeo:
    address: Optional[List[Address]] = None
    """Адрес"""
    newbuilding: Optional[Newbuilding] = None
    """Новостройки"""
    underground: Optional[Underground] = None
    """Метро"""


@dataclass
class OfferViewModel:
    id: int
    """ID объявления"""
    main_photo_url: Optional[str]
    """Основаная фотография объекта"""
    title: Optional[str]
    """Заголовок объявления"""
    url: str
    """URL объявления"""
    geo: OfferGeo
    """Гео"""
    subagent: Optional[Subagent]
    """Сабагент"""
    price_info: PriceInfo
    """Инофрмация о цене"""
    features: List[str]
    """Ключевые параметры: комиссии, бонусы, свободная продажа, ипотека"""
    publish_features: Optional[List[str]]
    """Параметры публикации: сколько осталось"""
    is_manual: bool
    """ Флаг 'из импорта'"""
    created_at: datetime
    """Дата подачи объявления"""
    archived_at: Optional[datetime]
    """Дата архивации"""
    status: Optional[str]
    """Строка статуса"""
