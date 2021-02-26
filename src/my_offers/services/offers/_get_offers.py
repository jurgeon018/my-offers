import asyncio
from typing import Any, Dict, List, Tuple

from cian_web.exceptions import BrokenRulesException, Error
from simple_settings import settings

from my_offers import entities, enums
from my_offers.entities import get_offers
from my_offers.helpers.page_info import get_page_info, get_pagination
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.offers_search_log import save_offers_search_log
from my_offers.services import offer_view
from my_offers.services.offers._degradation_handlers import (
    get_object_models_degradation_handler,
    get_object_models_total_count_degradation_handler,
)
from my_offers.services.offers.enrich.load_enrich_data import load_enrich_data
from my_offers.services.offers.enrich.prepare_enrich_params import prepare_enrich_params


async def prepare_data_for_get_offers(
        *,
        request: entities.GetOffersRequest,
        filters: Dict[str, Any],
        realty_user_id: int,
) -> Tuple[Dict[str, bool], List[get_offers.GetOfferV2], entities.PageInfo]:
    total_count_task = asyncio.create_task(get_object_models_total_count_degradation_handler(filters))
    limit, offset = get_pagination(request.pagination)
    object_models_result = await get_object_models_degradation_handler(
        filters=filters,
        limit=limit,
        offset=offset,
        sort_type=request.sort or enums.GetOffersSortType.by_default,
    )
    if object_models_result.degraded:
        raise BrokenRulesException([
            Error(
                message='Произошла ошибка при загрузке объявлений',
                code='degradation',
                key='object_models'
            )
        ])
    object_models = object_models_result.value
    offers, degradation = await get_offer_views(
        object_models=object_models,
        user_id=realty_user_id,
        status_tab=request.filters.status_tab
    )
    total_count_result = await total_count_task
    total = total_count_result.value
    if settings.LOG_SEARCH_QUERIES and filters.get('search_text'):
        await save_offers_search_log(filters=filters, found_cnt=total, is_error=object_models_result.degraded)

    return degradation, offers, get_page_info(limit=limit, offset=offset, total=total)


async def get_offer_views(
        *,
        object_models: List[ObjectModel],
        user_id: int,
        status_tab: enums.OfferStatusTab
) -> Tuple[List[get_offers.GetOfferV2], Dict[str, bool]]:
    # подготовка параметров для обогащения
    enrich_params = prepare_enrich_params(models=object_models, user_id=user_id)

    # получение данных для обогащения
    enrich_data, degradation = await load_enrich_data(params=enrich_params, status_tab=status_tab)

    # подготовка моделей для ответа
    offers = [
        offer_view.v2_build_offer_view(
            object_model=object_model,
            enrich_data=enrich_data
        )
        for object_model in object_models
    ]

    return offers, degradation
