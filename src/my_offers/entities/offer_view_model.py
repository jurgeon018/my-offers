from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers import enums


@dataclass
class PriceInfo:
    exact_price: str
    """Цена"""


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
    url: str
    """Поисковый запрос по ЖК"""


@dataclass
class Underground:
    region_id: int
    """ID региона"""
    line_color: str
    """Цвет линии метро"""
    name: str
    """Название метро"""
    url: str
    """Поисковый запрос по метро"""


@dataclass
class Address:
    name: str
    """Полный адрес"""
    url: str
    """Поисковый запрос по адресу"""


@dataclass
class OfferGeo:
    address: Optional[Address] = None
    """Адрес"""
    newbuilding: Optional[Newbuilding] = None
    """Новостройки"""
    underground: Optional[Underground] = None
    """Метро"""


@dataclass
class OfferViewModel:
    main_photo_url: Optional[str]
    """Основаная фотография объекта"""
    title: Optional[str]
    """Заголовок объявления"""
    url: Optional[str]
    """URL объявления"""
    geo: Optional[OfferGeo]
    """Гео"""
    subagent: Optional[Subagent]
    """Сабагент"""
    price_info: PriceInfo
    """Инофрмация о цене"""
    features: List[str]
    """Ключевые параметры: комиссии, бонусы, свободная продажа, ипотека"""
    publish_features: Optional[List[str]]
    """Параметры публикации: сколько осталось, автопродление"""
    vas: Optional[List[enums.Services]]
    """Список VAS'ов"""
    is_from_package: bool
    """ Флаг 'из пакета'
    """
    is_from_import: bool
    """ Флаг 'из импорта'
    """
    is_publication_time_ends: bool
    """ Флаг 'меньше суток до конца публикации'
    """
    created_at: Optional[datetime]
    """Дата подачи объявления"""
    id: Optional[int]
    """ID объявления"""
