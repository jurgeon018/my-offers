from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import DistrictInfo


def get_district_id(district_info: Optional[List[DistrictInfo]]) -> Optional[int]:
    if not district_info:
        return None

    parent_id_district_id = {}
    for item in district_info:
        parent_id_district_id[item.parent_id] = item.id

    current_id = None
    for _ in range(len(parent_id_district_id)):
        current_id = parent_id_district_id.get(current_id)

    return current_id
