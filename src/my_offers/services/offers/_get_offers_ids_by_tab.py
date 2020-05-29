from my_offers.entities import GetOffersIdsByTabRequest, GetOffersIdsByTabResponse
from my_offers.repositories.postgresql import offer
from my_offers.services.offers import get_user_filter


async def get_offers_ids_by_tab(request: GetOffersIdsByTabRequest) -> GetOffersIdsByTabResponse:
    filters = await get_user_filter(request.user_id)

    if request.with_subs:
        filters.pop('user_id', None)

    if not request.status_tab.is_all:
        filters['status_tab'] = request.status_tab.value

    ids = await offer.get_offers_ids_by_tab(filters)

    return GetOffersIdsByTabResponse(ids=ids)
