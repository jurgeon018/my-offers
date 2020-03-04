from attr import dataclass

from my_offers.enums import GetOfferStatusTab


@dataclass
class QaGetByIdRequest:
    offer_id: int
    status_tab: GetOfferStatusTab
