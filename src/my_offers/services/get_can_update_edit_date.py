from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.announcements import v1_can_update_editdate
from my_offers.repositories.announcements.entities import V1CanUpdateEditdate


_v1_can_update_editdate_degradation_handler = get_degradation_handler(
    func=v1_can_update_editdate,
    key='v1_can_update_editdate',
    default=[],
)


async def get_can_update_edit_date(ids: List[int]) -> Dict[int, bool]:
    response = await _v1_can_update_editdate_degradation_handler(V1CanUpdateEditdate(ids=ids))

    return {item.id: item.can_update_edit_date for item in response.value}
