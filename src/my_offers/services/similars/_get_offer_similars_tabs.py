import asyncio

from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import is_test
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.duplicates.helpers.range_price import get_range_price
from my_offers.services.duplicates.helpers.rooms_count import get_possible_room_counts
from my_offers.services.duplicates.helpers.tabs import get_tabs
from my_offers.services.offers import load_object_model


async def v1_get_offer_similars_tabs_public(
        request: entities.GetOfferDuplicatesTabsRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesTabsResponse:
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return entities.GetOfferDuplicatesTabsResponse(tabs=[])


    return entities.GetOfferDuplicatesTabsResponse(
        tabs=get_tabs(
            duplicate_count=duplicates_count,
            same_building_count=same_building_count,
            similar_count=similar_count
        ),
    )
