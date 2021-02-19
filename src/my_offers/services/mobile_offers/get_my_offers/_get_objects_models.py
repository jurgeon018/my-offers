from typing import Any, Dict, List, Tuple

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import get_object_models


async def get_object_models_with_pagination(
        *,
        filters: Dict[str, Any],
        limit: int,
        offset: int,
        sort_type: enums.MobOffersSortType,
) -> Tuple[List[ObjectModel], bool]:
    result: List[ObjectModel] = await get_object_models(
        filters=filters,
        limit=limit + 1,
        offset=offset,
        sort_type=sort_type,
    )

    can_load_more = len(result) > limit
    if can_load_more:
        result = result[:limit]

    return result, can_load_more
