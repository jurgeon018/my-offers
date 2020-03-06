from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import OfferViewModel, OfferViewModelV2
from my_offers.enums.sort_types import GetOffersSortType
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


@dataclass
class Filter:
    status_tab: enums.GetOfferStatusTab
    """Вкладка"""
    sort_type: Optional[GetOffersSortType]
    """Тип сортировки"""
    deal_type: Optional[enums.DealType]
    """Тип сделки"""
    offer_type: Optional[enums.OfferType]
    """Тип объявления"""
    services: Optional[List[Services]]
    """Тип размещения"""
    sub_agent_ids: Optional[List[int]]
    """Список сотрудников (только для мастрер аккаунтов)"""
    has_photo: Optional[bool]
    """Только с фото"""
    is_manual: Optional[bool]
    """Только ручные"""
    is_in_hidden_base: Optional[bool]
    """Только видимые агентам"""
    search_text: Optional[str]
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
class AvailableActions:
    can_update_edit_date: bool
    """Можно обновить дату"""
    can_move_to_archive: bool
    """Пользователь может перенести объявление в архив"""
    can_delete: bool
    """Можно ли удалить объялвение"""


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
    is_autoprolong: bool
    """Автопродление"""
    is_publication_time_ends: bool
    """ Флаг 'меньше суток до конца публикации'"""
    publish_features: Optional[List[str]]
    """Параметры публикации: сколько осталось"""
    auction: Optional[Auction] = None
    """Данные об аукционе по объявлению"""


@dataclass
class NotActiveInfo:
    status: str
    """Статус для некативных"""
    message: Optional[str] = None
    """Доп. сообщение"""


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
class GetOffer(OfferViewModel):
    statistics: Optional[Statistics]
    """Статистика по объявлению"""
    available_actions: AvailableActions
    """Доступные действия с объявлениями"""
    auction: Optional[Auction] = None
    """Данные об аукционе по объявлению"""
    moderation: Optional[Moderation] = None
    """Данные о причине отклонения объявления"""
    not_active_info: Optional[NotActiveInfo] = None
    """Доп. информация для вкладки неактивные"""


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
class GetOffersResponse:
    offers: List[GetOffer]
    """Список объявлений"""
    counters: OfferCounters
    """Счеткики количества объявлений"""
    page: PageInfo
    """Информация о странице"""
    degradation: Dict[str, bool]
    """Информация о деградации"""


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
