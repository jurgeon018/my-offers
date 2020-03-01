from attr import dataclass

from my_offers.enums.offer_action_status import OfferActionStatus


@dataclass
class OfferActionRequest:
    offer_id: int


@dataclass
class OfferActionResponse:
    status: OfferActionStatus
