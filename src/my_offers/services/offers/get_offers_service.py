from my_offers import entities
from my_offers.repositories import postgresql
from my_offers.services.offers.offer_view import build_offer_view


async def get_offers_private(request: entities.GetOffersPrivateRequest) -> entities.GetOffersResponse:
    """ Приватная апи получения моих объявлений. Требует явной передачи пользователя.
    """
    return await get_offers_public(
        request=request,
        user_id=request.user_id
    )


async def get_offers_public(request: entities.GetOffersRequest, user_id: int) -> entities.GetOffersResponse:
    """ Получить получить объявления для пользователя. Для м/а с учетом иерархии.
    """
    object_models = await postgresql.get_object_models(
        status_tab=request.status_tab,
        user_id=user_id
    )
    offers_views = [
        build_offer_view(raw_offer=object_model)
        for object_model in object_models
    ]

    return entities.GetOffersResponse(
        offers=offers_views,
        counters=entities.OfferCounters(
            active=1,
            not_active=0,
            declined=0,
            archived=0
        )
    )
