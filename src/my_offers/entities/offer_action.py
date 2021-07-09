from typing import List, Optional

from attr import dataclass

from my_offers.entities.get_offers import Filter
from my_offers.enums.actions import MassRestoreActionType, OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities.announcement_progress_dto import (
    State as OffersOperationStatus,
)


@dataclass
class OfferActionRequest:
    offer_id: int


@dataclass
class OfferActionResponse:
    status: OfferActionStatus


@dataclass
class OffersMassRestoreRequest:
    offers_ids: Optional[List[int]]
    """ID объявлений для восстановления"""
    action_type: MassRestoreActionType
    """Тип массовой операции"""
    filters: Filter
    """Фильтры"""


@dataclass
class OfferMassRestoreStatus:
    offer_id: int
    """ID объявления"""
    status: OffersOperationStatus
    """Статус восстановления объявления"""
    message: Optional[str]
    """Сообщение"""


@dataclass
class OffersMassRestoreCounters:
    draft_count: Optional[int] = None
    """Кол-во черновиков"""
    xml_count: Optional[int] = None
    """Кол-во выгрузочных объявленеий"""
    restored_count: Optional[int] = None
    """Кол-во восстановленных объявлений"""
    error_count: Optional[int] = None
    """Кол-во объявлений с ошибками"""


@dataclass
class OffersMassRestoreResponse:
    total: int
    """Общее количетсво офферов"""
    counters: OffersMassRestoreCounters
    """Счетчики по общему прогрессу"""
    offers: List[OfferMassRestoreStatus]
    """Статусы по восстановленным объявлениям"""
