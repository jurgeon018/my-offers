from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.monolith_cian_ms_announcements import v1_can_update_editdate
from my_offers.repositories.monolith_cian_ms_announcements.entities import V1CanUpdateEditdate


async def can_update_edit_date(ids: List[int]) -> Dict[int, bool]:
    response = await v1_can_update_editdate(V1CanUpdateEditdate(ids=ids))
    data = {item.id: bool(item.can_update_edit_date) for item in response}

    result = {}
    for offer_id in ids:
        result[offer_id] = data[offer_id] if offer_id in data else False

    return result


can_update_edit_date_degradation_handler = get_degradation_handler(
    func=can_update_edit_date,
    key='can_update_edit_date',
    default={},
)
