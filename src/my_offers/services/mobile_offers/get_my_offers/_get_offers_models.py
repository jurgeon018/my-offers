from typing import Any, Dict, List

from my_offers import entities, enums
from my_offers.repositories.postgresql.offer import get_offers_with_parsed_object_model


async def get_offers_with_object_model(
        *,
        filters: Dict[str, Any],
        limit: int,
        offset: int,
        sort_type: enums.MobOffersSortType,
) -> List[entities.OfferWithObjectModel]:
    return await get_offers_with_parsed_object_model(
        filters=filters,
        limit=limit,
        offset=offset,
        sort_type=sort_type,
    )
