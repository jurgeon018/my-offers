import math
from typing import Any, Dict, List, Optional, Tuple

from simple_settings import settings

from my_offers import entities
from my_offers.entities import get_offers
from my_offers.mappers.get_offers_request import get_offers_filters_mapper
from my_offers.repositories import postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.get_master_user_id import get_master_user_id
from my_offers.services.offer_view import build_offer_view
from my_offers.services.offers.enrich.load_enrich_data import load_enrich_data
from my_offers.services.offers.enrich.prepare_enrich_params import prepare_enrich_params


async def get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersResponse:
    """ Приватная апи получения моих объявлений. Требует явной передачи пользователя. """
    return await get_offers_public(
        request=request,
        realty_user_id=request.user_id
    )


async def get_offers_public(request: entities.GetOffersRequest, realty_user_id: int) -> entities.GetOffersResponse:
    """ Получить объявления для пользователя. Для м/а с учетом иерархии. """
    # шаг 1 - подготовка параметров запроса
    filters = await _get_filters(filters=request.filters, user_id=realty_user_id)
    limit, offset = _get_pagination(request.pagination)

    # шаг 2 - получение object models
    object_models, total = await postgresql.get_object_models(
        filters=filters,
        limit=limit,
        offset=offset,
        sort_type=request.sort or get_offers.GetOffersSortType.by_default,
    )

    offers, degradation = await get_offer_views(object_models)

    # шаг 3 - формирование ответа
    return entities.GetOffersResponse(
        offers=offers,
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
        ),
        degradation=degradation,
    )


async def get_offer_views(object_models: List[ObjectModel]) -> Tuple[List[get_offers.GetOffer], Dict[str, bool]]:
    # шаг 1 - подготовка параметров для обогащения
    enrich_params = prepare_enrich_params(object_models)

    # шаг 2 - получение данных для обогащения
    enrich_data, degradation = await load_enrich_data(enrich_params)

    # шаг 3 - подготовка моделей для ответа
    offers = [
        build_offer_view(object_model=object_model, enrich_data=enrich_data)
        for object_model in object_models
    ]

    return offers, degradation


async def _get_filters(*, user_id: int, filters: Optional[get_offers.Filter]) -> Dict[str, Any]:
    result: Dict[str, Any] = get_offers_filters_mapper.map_to(filters) if filters else []
    result['master_user_id'] = await get_master_user_id(user_id)
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
