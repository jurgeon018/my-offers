from typing import Any, Dict

from cian_core.degradation import DegradationResult

from my_offers import entities
from my_offers.services.offers import get_user_filter
from my_offers.services.offers._degradation_handlers import get_offer_counters_mobile_degradation_handler


async def v1_get_offers_counters_mobile_public(
        # TODO: Пока suspended до 2го релиза CD-100659
        request: entities.GetOffersCountersMobileRequest,
        realty_user_id: int,
) -> entities.GetOffersCountersMobileResponse:
    filters: Dict[str, Any] = await get_user_filter(realty_user_id)

    result: DegradationResult = await get_offer_counters_mobile_degradation_handler(filters)

    return result.value
