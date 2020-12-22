import asyncio
from typing import Dict, List, Tuple

from cian_web.exceptions import BrokenRulesException, Error
from simple_settings import settings

from my_offers import entities, enums
from my_offers.entities import get_offers
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.offers_search_log import save_offers_search_log
from my_offers.services import offer_view
from my_offers.services.offers._get_offers import (
    get_agent_hierarchy_data_degradation_handler,
    get_counter_filters,
    get_filters,
    get_object_models_degradation_handler,
    get_offer_counters_degradation_handler,
    get_page_info,
    get_pagination,
)
from my_offers.services.offers.enrich.load_enrich_data import load_enrich_data
from my_offers.services.offers.enrich.prepare_enrich_params import prepare_enrich_params


async def v2_get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersV2Response:
    """ Приватная апи получения моих объявлений. """
    return await v2_get_offers_public(
        request=request,
        realty_user_id=request.user_id
    )


async def v2_get_offers_public(request: entities.GetOffersRequest, realty_user_id: int) -> entities.GetOffersV2Response:
    """ Получить объявления для пользователя. Для м/а с учетом иерархии. """
    # шаг 1 - подготовка параметров запроса
    filters = await get_filters(filters=request.filters, user_id=realty_user_id)
    counter_filters = get_counter_filters(filters)
    limit, offset = get_pagination(request.pagination)

    # шаг 2 - получение object models и счетчиков
    object_models_result, offer_counters_result = await asyncio.gather(
        get_object_models_degradation_handler(
            filters=filters,
            limit=limit,
            offset=offset,
            sort_type=request.sort or enums.GetOffersSortType.by_default,
        ),
        get_offer_counters_degradation_handler(counter_filters),
    )
    if object_models_result.degraded:
        raise BrokenRulesException([
            Error(
                message='Произошла ошибка при загрузке объявлений',
                code='degradation',
                key='object_models'
            )
        ])

    object_models, total = object_models_result.value
    if settings.LOG_SEARCH_QUERIES and filters.get('search_text'):
        await save_offers_search_log(filters=filters, found_cnt=total, is_error=object_models_result.degraded)

    offers, degradation = await v2_get_offer_views(
        object_models=object_models,
        user_id=realty_user_id,
        status_tab=request.filters.status_tab
    )

    degradation['offer_counters'] = offer_counters_result.degraded

    # шаг 3 - формирование ответа
    return entities.GetOffersV2Response(
        offers=offers,
        counters=offer_counters_result.value,
        page=get_page_info(limit=limit, offset=offset, total=total),
        degradation=degradation,
    )


async def v2_get_offer_views(
        *,
        object_models: List[ObjectModel],
        user_id: int,
        status_tab: enums.OfferStatusTab
) -> Tuple[List[get_offers.GetOfferV2], Dict[str, bool]]:
    # подготовка параметров для обогащения
    enrich_params = prepare_enrich_params(models=object_models, user_id=user_id)

    # получение данных для обогащения
    enrich_data, degradation = await load_enrich_data(
        params=enrich_params,
        status_tab=status_tab
    )

    agent_hierarchy_data_result = await get_agent_hierarchy_data_degradation_handler(user_id)

    # подготовка моделей для ответа
    offers = [
        offer_view.v2_build_offer_view(
            agent_hierarchy_data=agent_hierarchy_data_result.value,
            object_model=object_model,
            enrich_data=enrich_data
        )
        for object_model in object_models
    ]

    return offers, degradation
