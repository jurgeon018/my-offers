from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers import enums
from my_offers.entities import AvailableActions
from my_offers.entities.page_info import MobilePageInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


@dataclass
class Filters:
    deal_type: Optional[enums.DealType]
    """Тип сделки"""
    offer_type: Optional[enums.OfferType]
    """Тип объекта недвижимости"""


@dataclass
class OfferComplaint:
    id: int
    """Id жалобы"""
    date: Optional[datetime]
    """Дата жалобы"""
    comment: str
    """Комментарий"""


@dataclass
class OfferDeactivatedService:
    description: Optional[str]
    """Текст, что именно отключилось и каким образом добиться возобновления услуг"""
    is_auto_restore_on_payment_enabled: bool
    """Включено ли автовозобновление публикации"""


@dataclass
class ConcurrencyType:
    is_active: bool
    """Активная вкладка"""
    name: str
    """Название"""
    type: str
    """Тип"""


@dataclass
class OfferAuction:
    increase_bets_positions_count: Optional[int]
    current_bet: Optional[float]
    note_bet: Optional[str]
    is_available_auction: Optional[bool]
    concurrency_types: Optional[List[ConcurrencyType]]
    is_strategy_enabled: bool
    is_fixed_bet: bool
    strategy_description: Optional[str]
    concurrency_type_title: Optional[str]


@dataclass
class OfferStats:
    competitors_count: Optional[int]
    """Oбщее количество дублей"""
    duplicates_count: Optional[int]
    """Новые дубли"""
    calls_count: Optional[int]
    """Количество звонков"""
    skipped_calls_count: Optional[int]
    """Количество пропущенных звонков"""
    total_views: Optional[int]
    """Все просмотры"""
    daily_views: Optional[int]
    """Просмотр за день"""
    favorites: Optional[int]
    """Количество попаданий в избранное"""


@dataclass
class MobPrice:
    value: float
    """Цена"""
    currency: Currency
    """Валюта"""


@dataclass
class MobOffer:
    offer_id: int
    """Id оффера"""
    cian_id: Optional[int]
    """ID объявления на ЦИАНе"""
    cian_user_id: int
    """Cian id юзера, создавшего оффер"""
    realty_user_id: int
    """Realty id юзера, создавшего оффер"""
    price: MobPrice
    """Цена"""
    status: enums.MobStatus
    """Статус объявления"""
    offer_type: enums.OfferType
    """Тип оффера"""
    deal_type: enums.DealType
    """Тип сделки"""
    category: Category
    """Категория оффера"""
    is_archived: bool
    """В архиве"""
    has_video_offence: bool
    """Есть ли видео нарушения"""
    has_photo_offence: bool
    """Есть ли фото нарушения"""
    is_object_on_premoderation: bool
    """На премодерации ли оффер"""
    identification_pending: bool
    is_auction: bool
    """В аукционе ли оффер"""
    formatted_price: str
    """Инфо о цене"""
    formatted_info: str
    """Описание"""
    formatted_address: str
    """Адрес"""
    description: str
    """Описание"""
    available_actions: AvailableActions
    """Доступные действия оффера"""
    services: List[Services]
    """Типы размещений оффера"""
    deactivated_service: Optional[OfferDeactivatedService]
    auction: Optional[OfferAuction]
    stats: Optional[OfferStats]
    """Cтатистика по офферу"""
    archived_date: Optional[datetime]
    """Дата попадания в архив"""
    photo: Optional[str]
    """Url фото"""
    publish_till_date: Optional[datetime]
    """Дата публикации"""
    complaints: Optional[List[OfferComplaint]]
    """Жалобы"""
    coworking_id: Optional[int]
    """Id коворкинга"""
    is_private_agent: bool
    """Является компанией (либо агент, либо частный маклер)"""
    is_declined: bool
    """Отклонено модератором"""


@dataclass
class MobileGetMyOffersRequest:
    limit: int
    """Лимит"""
    offset: int
    """Оффсет"""
    tab_type: enums.MobTabType
    """Таб для офферов"""
    filters: Optional[Filters]
    """Фильтры"""
    search: Optional[str]
    """Поисковая строка"""
    sort: Optional[enums.MobOffersSortType]
    """Сортировка"""


@dataclass
class MobileGetMyOffersResponse:
    page: MobilePageInfo
    """Информация о странице"""
    offers: List[MobOffer]
    """Список объявлений"""


@dataclass
class GetOffersCountersMobileRequest:
    search: Optional[str]
    """Полнотекстовый поиск по объявлению"""


@dataclass
class GetOffersCountersMobileCounter:
    total: Optional[int]
    """Количество всех объявлений"""
    flat: Optional[int]
    """Жилая"""
    suburban: Optional[int]
    """Загородная"""
    commercial: Optional[int]
    """Коммерческая"""


@dataclass
class GetOffersCountersMobileArchivedInactiveCounter:
    total: Optional[int]
    """Количество всех объявлений"""
    rent: Optional[int]
    """Аренда"""
    sale: Optional[int]
    """Продажа"""


@dataclass
class GetOffersCountersMobileResponseV1:
    rent: Optional[GetOffersCountersMobileCounter]
    """Вкладка аренда"""
    sale: Optional[GetOffersCountersMobileCounter]
    """Вкладка продажа"""
    archived: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка архивные"""
    inactive: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка Неактивные + Отклоненные"""


@dataclass
class GetOffersCountersMobileResponseV2:
    rent: Optional[GetOffersCountersMobileCounter]
    """Вкладка аренда"""
    sale: Optional[GetOffersCountersMobileCounter]
    """Вкладка продажа"""
    archived: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка архивные"""
    inactive: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка Неактивные"""
    declined: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка Отклоненные"""
