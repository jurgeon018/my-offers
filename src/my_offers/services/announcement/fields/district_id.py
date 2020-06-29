from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import DistrictInfo


def get_district_id(district_info: Optional[List[DistrictInfo]]) -> Optional[int]:
    if not district_info:
        return None
    district_id = 0

    for item in district_info:
        if item.parent_id and item.id > district_id:
            district_id = item.id

    if district_id != 0:
        return district_id
    return None
