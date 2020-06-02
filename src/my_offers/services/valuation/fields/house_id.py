from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type


def get_house_id(
        address: List[AddressInfo]
) -> Optional[int]:
    for detail in address:
        if detail.type == Type.house:
            return detail.id
    return None
