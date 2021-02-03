import math
from typing import Optional, Tuple

from simple_settings import settings

from my_offers import entities


def get_page_info(*, limit: int, offset: int, total: int) -> entities.PageInfo:
    return entities.PageInfo(
        count=total,
        can_load_more=total > offset + limit,
        page_count=math.ceil(total / limit)
    )


def get_pagination(pagination: Optional[entities.Pagination]) -> Tuple[int, int]:
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
