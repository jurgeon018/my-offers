from typing import Any, Dict, List, Optional, Tuple

from simple_settings import settings

from my_offers.entities import get_offers
from my_offers.mappers.get_offers_request import get_offers_filters_mapper
from my_offers.repositories.postgresql.agents import get_master_user_id


async def get_filters(*, user_id: int, filters: get_offers.Filter) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mapper.map_to(filters)
    result['master_user_id'] = await get_master_user_filter(user_id)

    return result


async def get_master_user_filter(user_id: int) -> List[int]:
    result = [user_id]
    master_user_id = await get_master_user_id(user_id)
    if master_user_id:
        result.append(master_user_id)

    return result


def get_pagination(pagination: Optional[get_offers.Pagination]) -> Tuple[int, int]:
    limit = settings.OFFER_LIST_LIMIT
    offset = 0

    if not pagination:
        return limit, offset

    if pagination.limit:
        limit = pagination.limit

    if pagination.offset:
        offset = pagination.offset
    elif pagination.page:
        offset = limit * (pagination.page - 1)

    return limit, offset
