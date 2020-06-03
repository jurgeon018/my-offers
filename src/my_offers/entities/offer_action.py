from typing import List, Optional

from attr import dataclass

from my_offers.entities.get_offers import Filter
from my_offers.enums.actions import ActionType, OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities.announcement_progress_dto import (
    State as OfferMassRestoreState,
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
    action_type: ActionType
    """Тип массовой операции"""
    filters: Filter
    """Фильтры"""


@dataclass
class OfferMassRestoreStatus:
    offer_id: int
    """ID объявления"""
    status: OfferMassRestoreState
    """Статус восстановления объявления"""
    message: Optional[str]
    """Сообщение"""


@dataclass
class OffersMassRestoreResponse:
    offers: List[OfferMassRestoreStatus]
    """Статусы по восстановленным объявлениям"""
