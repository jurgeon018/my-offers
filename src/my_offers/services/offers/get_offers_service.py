from typing import Optional

from my_offers.entities import GetOffersRequest, GetOffersResponse
from my_offers.entities.get_offers import OfferCounters
from my_offers.repositories import postgresql
from my_offers.services.offers.offer_view import build_offer_view


async def get_offers(request: GetOffersRequest, realty_user_id: Optional[int]) -> GetOffersResponse:
    """ Получить получить объявления для пользователя. Для м/а с учетом иерархии.
    """
    status_tab = request.status_tab

    if not realty_user_id:
        raise Exception('Не указан X-Real-UserId')

    raw_offers = await postgresql.get_offers_by_status(
        status_tab=status_tab,
        user_id=realty_user_id
    )
    offers = [
        build_offer_view(raw_offer=offer)
        for offer in raw_offers
    ]

    return GetOffersResponse(
        offers=offers,
        counters=OfferCounters(
            active=1,
            not_active=0,
            declined=0,
            archived=0
        )
    )
