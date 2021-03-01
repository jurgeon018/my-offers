from typing import Any, Dict, Optional

from my_offers import enums
from my_offers.entities import get_offers, mobile_offer
from my_offers.mappers.get_offers_request import (
    MOBILE_TAB_TYPE_TO_STATUS_TYPE,
    get_offers_filters_mapper,
    get_offers_filters_mobile_mapper,
)
from my_offers.repositories.postgresql import get_master_user_id
from my_offers.services.offers.helpers.search_text import prepare_search_text


async def get_filters(*, user_id: int, filters: get_offers.Filter) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mapper.map_to(filters)
    if filters.status_tab.is_all:
        del result['status_tab']

    user_filter = await get_user_filter(user_id)
    result.update(user_filter)

    if search_text := result.get('search_text'):
        result['search_text'] = prepare_search_text(search_text)

    return result


async def get_filters_mobile(
        *,
        user_id: int,
        filters: mobile_offer.Filters,
        tab_type: enums.MobTabType,
        search_text: Optional[str],
) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mobile_mapper.map_to(filters) or {}

    user_filter: Dict[str, Any] = await get_user_filter(user_id)
    result.update(user_filter)

    result['status_tab'] = MOBILE_TAB_TYPE_TO_STATUS_TYPE[tab_type]

    if search_text:
        result['search_text'] = prepare_search_text(search_text)

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


def get_counter_filters(filters):
    counter_filters = {
        'master_user_id': filters.get('master_user_id'),
        'user_id': filters.get('user_id'),
    }
    if search_text := filters.get('search_text'):
        counter_filters['search_text'] = search_text

    return counter_filters
