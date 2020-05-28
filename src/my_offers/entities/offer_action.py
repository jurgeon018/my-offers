from typing import List, Optional

from attr import dataclass

from my_offers.enums.offer_action_status import ActionType, OfferActionStatus
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
    action_type: ActionType


@dataclass
class OfferMassRestoreStatus:
    offer_id: int
    status: OfferMassRestoreState
    message: Optional[str]


@dataclass
class OffersMassRestoreResponse:
    offers: List[OfferMassRestoreStatus]
