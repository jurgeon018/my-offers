from typing import Any, Dict, Optional, Tuple

from simple_settings import settings

from my_offers.entities import get_offers
from my_offers.mappers.get_offers_request import get_offers_filters_mapper
from my_offers.repositories.postgresql.agents import get_master_user_id


async def get_filters(*, user_id: int, filters: get_offers.Filter) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mapper.map_to(filters)
    user_filter = await get_user_filter(user_id)
    result.update(user_filter)

    return result


async def get_user_filter(user_id: int) -> Dict[str, Any]:
    master_user_id = await get_master_user_id(user_id)
    user_filter: Dict[str, Any] = {}
    if master_user_id:
        # опубликовал мастер или сотрудник и объявление назначено на сотрудника
        user_filter['master_user_id'] = [master_user_id, user_id]
        user_filter['user_id'] = user_id
    else:
        user_filter['master_user_id'] = user_id

    return user_filter


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
