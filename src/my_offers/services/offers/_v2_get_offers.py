import math
from typing import Dict, List, Tuple

from my_offers import entities, enums
from my_offers.entities import get_offers
from my_offers.repositories import postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.offer import get_offer_counters
from my_offers.services.offer_view import v2_build_offer_view
from my_offers.services.offers._get_offers import get_filters, get_pagination
from my_offers.services.offers.enrich.load_enrich_data import load_enrich_data
from my_offers.services.offers.enrich.prepare_enrich_params import prepare_enrich_params


async def v2_get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersV2Response:
    """ Приватная апи получения моих объявлений. Требует явной передачи пользователя. """
    return await v2_get_offers_public(
        request=request,
        realty_user_id=request.user_id
    )


async def v2_get_offers_public(request: entities.GetOffersRequest, realty_user_id: int) -> entities.GetOffersV2Response:
    """ Получить объявления для пользователя. Для м/а с учетом иерархии. """
    # шаг 1 - подготовка параметров запроса
    filters = await get_filters(filters=request.filters, user_id=realty_user_id)
    limit, offset = get_pagination(request.pagination)

    # шаг 2 - получение object models
    object_models, total = await postgresql.get_object_models(
        filters=filters,
        limit=limit,
        offset=offset,
        sort_type=request.sort or enums.GetOffersSortType.by_default,
    )

    offers, degradation = await v2_get_offer_views(object_models=object_models, user_id=realty_user_id)

    # шаг 3 - формирование ответа
    counter_filters = {
        'master_user_id': filters.get('master_user_id'),
        'user_id': filters.get('user_id'),
    }

    return entities.GetOffersV2Response(
        offers=offers,
        counters=await get_offer_counters(counter_filters),
        page=get_offers.PageInfo(
            count=total,
            can_load_more=total > offset + limit,
            page_count=math.ceil(total / limit)
        ),
        degradation=degradation,
    )


async def v2_get_offer_views(
        *,
        object_models: List[ObjectModel],
        user_id: int,
) -> Tuple[List[get_offers.GetOfferV2], Dict[str, bool]]:
    # шаг 1 - подготовка параметров для обогащения
    enrich_params = prepare_enrich_params(models=object_models, user_id=user_id)

    # шаг 2 - получение данных для обогащения
    enrich_data, degradation = await load_enrich_data(enrich_params)

    # шаг 3 - подготовка моделей для ответа
    offers = [
        v2_build_offer_view(object_model=object_model, enrich_data=enrich_data)
        for object_model in object_models
    ]

    return offers, degradation
