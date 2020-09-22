import math
from typing import Any, Dict, Optional, Tuple

from cian_core.degradation import get_degradation_handler
from simple_settings import settings

from my_offers.entities import get_offers
from my_offers.entities.get_offers import OfferCounters
from my_offers.mappers.get_offers_request import get_offers_filters_mapper
from my_offers.repositories import postgresql
from my_offers.repositories.postgresql import get_object_models, get_offers_offence
from my_offers.repositories.postgresql.agents import get_agent_names, get_master_user_id, is_master_agent
from my_offers.repositories.postgresql.billing import get_offers_payed_till
from my_offers.repositories.postgresql.offer import get_offer_counters, get_offers_payed_by, get_offers_update_at
from my_offers.repositories.postgresql.offer_import_error import get_last_import_errors
from my_offers.repositories.postgresql.offer_premoderation import get_offer_premoderations
from my_offers.services import statistics
from my_offers.services.offers.helpers.search_text import prepare_search_text


get_object_models_degradation_handler = get_degradation_handler(
    func=get_object_models,
    key='psql.get_object_models',
    default=([], 0),
)

get_offer_counters_degradation_handler = get_degradation_handler(
    func=get_offer_counters,
    key='psql.get_offer_counters',
    default=OfferCounters(
        active=None,
        not_active=None,
        declined=None,
        archived=None,
    ),
)

get_offers_offence_degradation_handler = get_degradation_handler(
    func=get_offers_offence,
    key='psql.get_offers_offence',
    default=[],
)

get_last_import_errors_degradation_handler = get_degradation_handler(
    func=get_last_import_errors,
    key='psql.get_last_import_errors',
    default=dict(),
)

get_agent_names_degradation_handler = get_degradation_handler(
    func=get_agent_names,
    key='psql.get_agent_names',
    default=[],
)

is_master_agent_degradation_handler = get_degradation_handler(
    func=is_master_agent,
    key='psql.is_master_agent',
    default=False,
)

get_offer_premoderations_degradation_handler = get_degradation_handler(
    func=get_offer_premoderations,
    key='psql.get_offer_premoderations',
    default=[],
)

get_offers_update_at_degradation_handler = get_degradation_handler(
    func=get_offers_update_at,
    key='psql.get_offers_update_at',
    default=dict(),
)

get_offers_payed_till_degradation_handler = get_degradation_handler(
    func=get_offers_payed_till,
    key='psql.get_offers_payed_till',
    default=dict(),
)

get_similars_counters_by_offer_ids_degradation_handler = get_degradation_handler(
    func=postgresql.get_similars_counters_by_offer_ids,
    key='psql.get_similars_counters_by_offer_ids',
    default=dict(),
)

get_offers_payed_by_degradation_handler = get_degradation_handler(
    func=get_offers_payed_by,
    key='psql.get_offers_payed_by',
    default=dict(),
)


get_views_counts_degradation_handler = get_degradation_handler(
    func=statistics.get_views_counts,
    key='cassandra.get_views_counts',
    default=dict(),
)

get_searches_counts_degradation_handler = get_degradation_handler(
    func=statistics.get_searches_counts,
    key='cassandra.get_searches_counts',
    default=dict(),
)

get_favorites_counts_degradation_handler = get_degradation_handler(
    func=statistics.get_favorites_counts,
    key='cassandra.get_favorites_counts',
    default=dict(),
)


async def get_filters(*, user_id: int, filters: get_offers.Filter) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mapper.map_to(filters)
    if filters.status_tab.is_all:
        del result['status_tab']

    user_filter = await get_user_filter(user_id)
    result.update(user_filter)

    if search_text := result.get('search_text'):
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


def get_page_info(*, limit: int, offset: int, total: int) -> get_offers.PageInfo:
    return get_offers.PageInfo(
        count=total,
        can_load_more=total > offset + limit,
        page_count=math.ceil(total / limit)
    )
