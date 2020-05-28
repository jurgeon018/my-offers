from my_offers.entities import GetOffersCountByTabRequest, GetOffersCountByTabResponse
from my_offers.repositories.postgresql import offer
from my_offers.repositories.postgresql.agents import get_master_user_id


async def get_offers_count_by_tab(request: GetOffersCountByTabRequest) -> GetOffersCountByTabResponse:
    filters = {}

    if request.with_subs and (master_user_id := await get_master_user_id(request.user_id)):
        filters['master_user_id'] = master_user_id
    else:
        filters['user_id'] = request.user_id

    if not request.status_tab.is_all:
        filters['status_tab'] = request.status_tab.value

    count = await offer.get_offers_count_by_tab(filters)

    return GetOffersCountByTabResponse(count=count)
