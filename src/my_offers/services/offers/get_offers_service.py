import asyncio

from simple_settings import settings

from my_offers import entities
from my_offers.mappers.get_offers_request import get_offers_request_mapper
from my_offers.repositories import postgresql
from my_offers.services.offer_view import build_offer_view


async def get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersResponse:
    """ Приватная апи получения моих объявлений. Требует явной передачи пользователя. """
    return await get_offers_public(
        request=request,
        user_id=request.user_id
    )


async def get_offers_public(request: entities.GetOffersRequest, user_id: int) -> entities.GetOffersResponse:
    """ Получить получить объявления для пользователя. Для м/а с учетом иерархии. """
    filters = get_offers_request_mapper.map_to(request)
    filters['master_user_id'] = user_id  # todo определение мастрер аккаунта https://jira.cian.tech/browse/CD-73807

    limit = settings.OFFER_LIST_LIMIT
    offset = limit * (request.page - 1) if request.page else 0

    object_models = await postgresql.get_object_models(
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
        counters=entities.OfferCounters(
            active=1,
            not_active=0,
            declined=0,
            archived=0
        )
    )
