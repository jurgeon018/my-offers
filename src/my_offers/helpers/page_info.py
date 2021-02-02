import math
from typing import Optional, Tuple

from simple_settings import settings

import my_offers.entities
import my_offers.entities.page_info


def get_page_info(*, limit: int, offset: int, total: int) -> my_offers.entities.page_info.PageInfo:
    return my_offers.entities.page_info.PageInfo(
        count=total,
        can_load_more=total > offset + limit,
        page_count=math.ceil(total / limit)
    )


def get_pagination(pagination: Optional[my_offers.entities.page_info.Pagination]) -> Tuple[int, int]:
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
