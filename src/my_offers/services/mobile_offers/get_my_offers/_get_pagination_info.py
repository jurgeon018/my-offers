from typing import Any, Dict

from my_offers.services.offers._degradation_handlers import get_object_models_total_count_degradation_handler


async def get_can_load_more(
        *,
        filters: Dict[str, Any],
        limit: int,
        offset: int,
) -> bool:
    total: int = (await get_object_models_total_count_degradation_handler(filters)).value
    return total > offset + limit
