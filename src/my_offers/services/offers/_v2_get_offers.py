import asyncio

from my_offers import entities
from my_offers.services.offers import get_filters
from my_offers.services.offers._degradation_handlers import get_offer_counters_degradation_handler
from my_offers.services.offers._filters import get_counter_filters
from my_offers.services.offers._get_offers import prepare_data_for_get_offers


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
    offer_counters_task = asyncio.create_task(get_offer_counters_degradation_handler(counter_filters))

    # шаг 2 - получение object models и счетчиков
    degradation, offers, page_info = await prepare_data_for_get_offers(
        filters=filters,
        realty_user_id=realty_user_id,
        request=request
    )

    offer_counters_result = await offer_counters_task
    degradation['offer_counters'] = offer_counters_result.degraded

    # шаг 3 - формирование ответа
    return entities.GetOffersV2Response(
        offers=offers,
        counters=offer_counters_result.value,
        page=page_info,
        degradation=degradation,
    )
