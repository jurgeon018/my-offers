from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.monolith_cian_ms_announcements import v1_can_update_editdate, v1_update_editdate
from my_offers.repositories.monolith_cian_ms_announcements.entities import UpdateEditdateRequest, V1CanUpdateEditdate


_v1_can_update_editdate_degradation_handler = get_degradation_handler(
    func=v1_can_update_editdate,
    key='v1_can_update_editdate',
    default=[],
)


_v1_update_editdate_degradation_handler = get_degradation_handler(
    func=v1_update_editdate,
    key='v1_update_editdate',
    default=[],
)


async def can_update_edit_date(ids: List[int]) -> Dict[int, bool]:
    response = await _v1_can_update_editdate_degradation_handler(V1CanUpdateEditdate(ids=ids))

    return {item.id: item.can_update_edit_date for item in response.value}


async def update_edit_date(ids: List[int]) -> Dict[int, bool]:
    response = await _v1_update_editdate_degradation_handler(UpdateEditdateRequest(ids=ids))
    data = {item.id: item.result for item in response.value}

    result = {}
    for offer_id in ids:
        if offer_id in data:
            result[offer_id] = data[offer_id].is_success
        else:
            result[offer_id] = False

    return result
