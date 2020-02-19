import asyncio
import math
from typing import Any, Dict, Optional, Tuple

from simple_settings import settings

from my_offers import entities
from my_offers.entities import get_offers
from my_offers.mappers.get_offers_request import get_offers_filters_mapper
from my_offers.repositories import postgresql
from my_offers.services.offer_view import build_offer_view


async def get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersResponse:
    """ Приватная апи получения моих объявлений. Требует явной передачи пользователя. """
    return await get_offers_public(
        request=request,
        realty_user_id=request.user_id
    )


async def get_offers_public(request: entities.GetOffersRequest, realty_user_id: int) -> entities.GetOffersResponse:
    """ Получить получить объявления для пользователя. Для м/а с учетом иерархии. """
    filters = _get_filters(filters=request.filters, user_id=realty_user_id)
    limit, offset = _get_pagination(request.pagination)

    object_models, total = await postgresql.get_object_models(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    futures = [
        build_offer_view(object_model=object_model)
        for object_model in object_models
    ]
    offers_views = await asyncio.gather(*futures)

    return entities.GetOffersResponse(
        offers=offers_views,
        counters=get_offers.OfferCounters(
            active=1,
            not_active=0,
            declined=0,
            archived=0
        ),
        page=get_offers.PageInfo(
            count=total,
            can_load_more=total > offset + limit,
            page_count=math.ceil(total / limit)
        )
    )


def _get_filters(*, user_id: int, filters: Optional[get_offers.Filter]) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mapper.map_to(filters) if filters else []
    result['master_user_id'] = user_id  # todo определение мастрер аккаунта https://jira.cian.tech/browse/CD-73807

    return result


def _get_pagination(pagination: Optional[get_offers.Pagination]) -> Tuple[int, int]:
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
