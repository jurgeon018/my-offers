from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers import enums
from my_offers.entities import AvailableActions
from my_offers.entities.page_info import MobilePageInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status


@dataclass
class Filters:
    deal_type: enums.DealType
    """Тип сделки"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""


@dataclass
class OfferComplaint:
    id: int
    """Id жалобы"""
    date: datetime
    """Дата жалобы"""
    comment: str
    """Комментарий"""
    reason_text: str
    """Причина"""
    decline: bool
    """Отклонена"""


@dataclass
class OfferDeactivatedService:
    description: str
    is_auto_restore_on_payment_enabled: bool


@dataclass
class OfferAuction:
    increase_bets_positions_count: int
    current_bet: float
    note_bet: str
    is_available_auction: bool
    concurrencyTypes: List[str]  # тип пока не указан в контракте
    type: str
    name: str
    is_active: bool
    is_strategy_enabled: bool
    is_fixed_bet: bool
    strategy_description: str
    concurrency_type_title: str


@dataclass
class OfferStats:
    competitors_count: int
    """Oбщее количество дублей"""
    duplicates_count: int
    """Новые дубли"""
    calls_count: int
    """Количество звонков"""
    skipped_calls_count: int
    """Количество пропущенных звонков"""
    total_views: int
    """Все просмотры"""
    daily_views: int
    """Просмотр за день"""
    favorites: int
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
    price: MobPrice
    """Цена"""
    status: Status
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
    services: List[enums.OfferServices]
    """Типы размещений оффера"""
    deactivated_service: Optional[OfferDeactivatedService]
    auction: Optional[OfferAuction]
    stats: Optional[OfferStats]
    """Cтатистика по офферу"""
    archived_date: Optional[datetime]
    """Дата попадания в архив"""
    photo: Optional[str]
    """Url фото"""
    publish_till_date: Optional[str]
    """Дата публикации"""
    complaints: Optional[List[OfferComplaint]]
    """Жалобы"""


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
class GetOffersCountersMobileResponse:
    rent: Optional[GetOffersCountersMobileCounter]
    """Вкладка аренда"""
    sale: Optional[GetOffersCountersMobileCounter]
    """Вкладка продажа"""
    archived: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка архивные"""
    inactive: Optional[GetOffersCountersMobileArchivedInactiveCounter]
    """Вкладка Неактивные + Отклоненные"""
