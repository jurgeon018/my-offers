

from my_offers import entities
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates_count
from my_offers.services.duplicates.helpers.tabs import get_tabs
from my_offers.services.duplicates.helpers.validation_offer import validate_offer
from my_offers.services.offers import load_object_model


async def v1_get_offer_duplicates_tabs_public(
        request: entities.GetOfferDuplicatesTabsRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesTabsResponse:
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)

    if not validate_offer(status=object_model.status, category=object_model.category):
        return entities.GetOfferDuplicatesTabsResponse(tabs=[])

    total = await get_offer_duplicates_count(request.offer_id)
    if total == 0:
        return entities.GetOfferDuplicatesTabsResponse(tabs=[])

    return entities.GetOfferDuplicatesTabsResponse(
        tabs=get_tabs(total),
    )
