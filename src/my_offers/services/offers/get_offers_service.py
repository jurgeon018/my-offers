from typing import Optional

from my_offers.entities import GetOffersRequest, GetOffersResponse
from my_offers.entities.get_offers import OfferCounters
from my_offers.repositories import postgresql
from my_offers.services.offers.offer_view import build_offer_view


async def get_offers(request: GetOffersRequest, realty_user_id: int) -> GetOffersResponse:
    """ Получить получить объявления для пользователя. Для м/а с учетом иерархии.
    """
    status_tab = request.status_tab

    object_models = await postgresql.get_object_models(
        status_tab=status_tab,
        user_id=realty_user_id
    )
    offers_views = [
        build_offer_view(raw_offer=object_model)
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
