from typing import List

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo


def get_address(
        address: List[AddressInfo]
) -> str:
    address_full_names = []
    for detail in address:
        if detail.full_name:
            address_full_names.append(detail.full_name)
    return ', '.join(address_full_names)
