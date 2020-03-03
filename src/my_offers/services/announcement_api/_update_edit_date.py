from typing import Dict, List

from my_offers.repositories.monolith_cian_ms_announcements import v1_update_editdate
from my_offers.repositories.monolith_cian_ms_announcements.entities import UpdateEditdateRequest


async def update_edit_date(ids: List[int]) -> Dict[int, bool]:
    response = await v1_update_editdate(UpdateEditdateRequest(ids=ids))
    data = {item.id: item.result for item in response}

    result = {}
    for offer_id in ids:
        if offer_id in data:
            result[offer_id] = data[offer_id].is_success
        else:
            result[offer_id] = False

    return result
