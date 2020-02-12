from my_offers.entities import GetOffersRequest, GetOffersResponse
from my_offers.entities.get_offers import GetOffersPrivateRequest, OfferCounters
from my_offers.enums import GetOfferStatusTab
from my_offers.repositories import postgresql
from my_offers.services.offers.offer_view import build_offer_view


async def get_offers_public(request: GetOffersRequest, realty_user_id: int) -> GetOffersResponse:
    """ Публичная апи получения моих объявлений.
    """
    return await _get_offers(
        status_tab=request.status_tab,
        user_id=realty_user_id
    )


async def get_offers_private(request: GetOffersPrivateRequest) -> GetOffersResponse:
    """ Приватная апи получения моих объявлений. Требует явной передачи пользователя.
    """
    return await _get_offers(
        status_tab=request.status_tab,
        user_id=request.user_id
    )


async def _get_offers(*, status_tab: GetOfferStatusTab, user_id: int) -> GetOffersResponse:
    """ Получить получить объявления для пользователя. Для м/а с учетом иерархии.
    """
    object_models = await postgresql.get_object_models(
        status_tab=status_tab,
        user_id=user_id
    )
    offers_views = [
        build_offer_view(object_model=object_model)
        for object_model in object_models
    ]

    return GetOffersResponse(
        offers=offers_views,
        counters=OfferCounters(
            active=1,
            not_active=0,
            declined=0,
            archived=0
        )
    )
