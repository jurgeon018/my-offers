from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers import enums
from my_offers.entities.page_info import PageInfo, Pagination
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


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
class MobOffer:
    offer_id: int
    """Id оффера"""
    status: Status
    """Статус объявления"""
    offer_type: enums.OfferType
    """Тип оффера"""
    deal_type: enums.DealType
    """Тип сделки"""
    is_archived: bool
    """В архиве"""
    archived_date: Optional[datetime]
    """Дата попадания в архив"""
    photo: Optional[str]
    """Url фото"""


    publish_till_date: Optional[str]
    """Узнать чего это такое"""
    complaints: Optional[OfferComplaint]






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
    page: PageInfo
    """Информация о странице"""
    offers: