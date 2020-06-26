from typing import Optional, List

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo


def get_house_id(address: Optional[List[AddressInfo]]) -> Optional[int]:
    if not address:
        return None

    for item in address:
        if item.type and item.type.is_house and item.id:
            return item.id

    return None
