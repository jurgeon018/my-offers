from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities import Geo


def get_address(
        geo: Geo
) -> str:
    address_full_names = []
    for detail in geo.address:
        if detail.full_name:
            address_full_names.append(detail.full_name)
    return ', '.join(address_full_names)
