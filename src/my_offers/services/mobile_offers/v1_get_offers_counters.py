from typing import Any, Dict

from cian_core.degradation import DegradationResult

from my_offers import entities
from my_offers.services.offers import get_user_filter
from my_offers.services.offers._degradation_handlers import get_offer_counters_mobile_v1_degradation_handler


async def v1_get_offers_counters_mobile_public(
        request: entities.GetOffersCountersMobileRequest,
        realty_user_id: int,
) -> entities.GetOffersCountersMobileResponseV1:
    filters: Dict[str, Any] = await get_user_filter(realty_user_id)
    if request.search:
        filters['search_text'] = request.search

    result: DegradationResult = await get_offer_counters_mobile_v1_degradation_handler(filters)

    return result.value
