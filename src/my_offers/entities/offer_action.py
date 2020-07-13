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
class OffersMassRestoreResponse:
    total: int
    """Общее количетсво офферов"""
    offers: List[OfferMassRestoreStatus]
    """Статусы по восстановленным объявлениям"""


@dataclass
class OffersChangePublisherStatus:
    offer_id: int
    """ID объявления"""
    status: OffersOperationStatus
    """Статус объявления"""
    message: Optional[str] = None
    """Сообщение"""


@dataclass
class OffersChangePublisherRequest:
    user_id: int
    """Пользователь на которого назвачить объявление"""
    offers_ids: List[int]
    """ID объявлений для которых надо сменить владельца"""


@dataclass
class OffersChangePublisherResponse:
    offers: List[OffersChangePublisherStatus]
    """Статусы по объявлениям"""
