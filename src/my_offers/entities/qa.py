from attr import dataclass

from my_offers.enums import OfferStatusTab


@dataclass
class QaGetByIdRequest:
    offer_id: int
    user_id: int
    status_tab: OfferStatusTab
