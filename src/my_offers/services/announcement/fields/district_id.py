from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import DistrictInfo


def get_district_id(district_info: Optional[List[DistrictInfo]]) -> Optional[int]:
    if not district_info:
        return None

    for item in district_info:
        if item.type and item.type.is_raion and item.id:
            return item.id

    for item in district_info:
        if item.type and item.type.is_mikroraion and item.id:
            return item.id

    for item in district_info:
        if item.type and item.type.is_poselenie and item.id:
            return item.id

    return None
