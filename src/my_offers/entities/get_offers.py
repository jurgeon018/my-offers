from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from my_offers import enums
from my_offers.entities.available_actions import AvailableActions
from my_offers.entities.offer_view_model import OfferViewModelV2
from my_offers.enums.not_active_status import NotActiveStatus


@dataclass
class Filter:
    status_tab: enums.OfferStatusTab
    """Вкладка"""
    deal_type: Optional[enums.DealType] = None
    """Тип сделки"""
    offer_type: Optional[enums.OfferType] = None
    """Тип объявления"""
    services: Optional[List[enums.OfferServices]] = None
    """Тип размещения"""
    sub_agent_ids: Optional[List[int]] = None
    """Список сотрудников (только для мастрер аккаунтов)"""
    has_photo: Optional[bool] = None
    """Только с фото"""
    is_manual: Optional[bool] = None
    """Только ручные"""
    is_in_hidden_base: Optional[bool] = None
    """Только видимые агентам"""
    search_text: Optional[str] = None
    """Полнотекстовый поиск по объявлению"""


@dataclass
class Pagination:
    page: Optional[int]
    """Номер страницы начиная с 1"""
    limit: Optional[int]
    """Количество объявлений на страницу"""
    offset: Optional[int]
    """Отступ от начала"""


@dataclass
class GetOffersRequest:
    filters: Filter
    """Параметры фильтрации"""
    pagination: Optional[Pagination]
    """Параметры страницы"""
    sort: Optional[enums.GetOffersSortType]
    """Сортировка"""


@dataclass
class GetOffersPrivateRequest(GetOffersRequest):
    user_id: int
    """ID пользователя"""


@dataclass
class Statistics:
    shows: Optional[int] = None
    """Количество показов в поиске"""
    views: Optional[int] = None
    """Количество просмотров карточки"""
    favorites: Optional[int] = None
    """Количество добавлений в избранное"""


@dataclass
class Auction:
    bet: Optional[int] = None
    """Текущая ставка аукциона"""
    district_place: Optional[int] = None
    """Позиция конкуренции по району"""
    home_place: Optional[int] = None
    """Позиция конкуренции по дому"""


@dataclass
class NotActiveInfo:
    status: str
    """Статус для неактивных"""
    message: Optional[str] = None
    """Доп. сообщение"""
    status_type: Optional[NotActiveStatus] = None
    """Тип статуса"""


@dataclass
class Moderation:
    declined_date: Optional[datetime] = None
    """Дата отклонения"""
    is_declined: Optional[bool] = None
    """Отклонено ли модератором"""
    reason: Optional[str] = None
    """Текст причины отклонения"""
    offence_status: Optional[str] = None
    """Статус модерации"""


@dataclass
class ActiveInfo:
    vas: List[enums.OfferVas]
    """Список VAS'ов"""
    is_from_package: bool
    """ Флаг 'из пакета'"""
    is_publication_time_ends: bool
    """ Флаг 'меньше суток до конца публикации'"""
    publish_features: Optional[List[str]]
    """Параметры публикации: сколько осталось"""
    auction: Optional[Auction] = None
    """Данные об аукционе по объявлению"""
    payed_till: Optional[datetime] = None
    """Дата, до которой оплачено размещение"""
    duplicates_count: Optional[int] = None
    """Количество дублей по объявлению"""
    same_building_count: Optional[int] = None
    """Количество 'в этом доме' по объявлению"""


@dataclass
class DeclinedInfo:
    moderation: Optional[Moderation] = None
    """Данные о причине отклонения объявления"""


@dataclass
class PageSpecificInfo:
    active_info: Optional[ActiveInfo] = None
    """Доп. информация для вкладки активные"""
    not_active_info: Optional[NotActiveInfo] = None
    """Доп. информация для вкладки неактивные"""
    declined_info: Optional[DeclinedInfo] = None
    """Доп. информация для вкладки отклоненные"""


@dataclass
class GetOfferV2(OfferViewModelV2):
    statistics: Optional[Statistics]
    """Статистика по объявлению"""
    available_actions: AvailableActions
    """Доступные действия с объявлениями"""
    page_specific_info: PageSpecificInfo
    """Данные зависящие от конкретной вкладки"""


@dataclass
class OfferCounters:
    active: Optional[int]
    not_active: Optional[int]
    declined: Optional[int]
    archived: Optional[int]


@dataclass
class PageInfo:
    count: int
    """Количество  объектов"""
    can_load_more: bool
    """Это не последняя страница"""
    page_count: int
    """Количество страниц"""


@dataclass
class GetOffersV2Response:
    offers: List[GetOfferV2]
    """Список объявлений"""
    counters: OfferCounters
    """Счеткики количества объявлений"""
    page: PageInfo
    """Информация о странице"""
    degradation: Dict[str, bool]
    """Информация о деградации"""
