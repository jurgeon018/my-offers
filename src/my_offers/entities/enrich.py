from dataclasses import dataclass
from typing import List

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info


@dataclass
class AddressUrlParams:
    deal_type: enums.DealType
    offer_type: enums.OfferType
    address_info: List[address_info.AddressInfo]
