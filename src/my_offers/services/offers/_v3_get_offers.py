from my_offers import entities
from my_offers.services.offers import get_filters
from my_offers.services.offers._get_offers import prepare_data_for_get_offers


async def v3_get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersV3Response:
    """ Приватная апи получения моих объявлений. """
    return await v3_get_offers_public(
        request=request,
        realty_user_id=request.user_id
    )


async def v3_get_offers_public(request: entities.GetOffersRequest, realty_user_id: int) -> entities.GetOffersV3Response:
    """ Получить объявления для пользователя. Для м/а с учетом иерархии. """
    # шаг 1 - подготовка параметров запроса
    filters = await get_filters(filters=request.filters, user_id=realty_user_id)

    # шаг 2 - получение object models и счетчиков
    degradation, offers, page_info = await prepare_data_for_get_offers(
        filters=filters,
        realty_user_id=realty_user_id,
        request=request
    )

    # шаг 3 - формирование ответа
    return entities.GetOffersV3Response(
        offers=offers,
        page=page_info,
        degradation=degradation,
    )
