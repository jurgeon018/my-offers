import asyncio

from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.repositories.postgresql.offers_duplicates import (
    get_offer_duplicates_ids,
    get_offers_in_same_building_count,
    get_similar_offers_count,
)
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.announcement.fields.is_test import get_is_test
from my_offers.services.duplicates.helpers.range_price import get_range_price
from my_offers.services.duplicates.helpers.rooms_count import get_possible_room_counts
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

    _, deal_type = get_types(object_model.category)
    district_id = get_district_id(object_model.geo.district)
    house_id = get_house_id(object_model.geo.address)
    rooms_list = get_possible_room_counts(object_model.rooms_count)
    low_price, high_price = get_range_price(
        bargain_terms=object_model.bargain_terms,
        total_area=object_model.total_area
    )
    is_test = get_is_test(object_model)
    duplicates_ids = await get_offer_duplicates_ids(object_model.id)
    duplicates_count = len(duplicates_ids)
    duplicates_ids.append(object_model.id)

    same_building_count, similar_count = await asyncio.gather(
        get_offers_in_same_building_count(
            deal_type=deal_type, house_id=house_id, rooms_counts=rooms_list, low_price=low_price,
            high_price=high_price, duplicates_ids=duplicates_ids, is_test=is_test,
        ),
        get_similar_offers_count(
            deal_type=deal_type, district_id=district_id, house_id=house_id, rooms_counts=rooms_list,
            low_price=low_price, high_price=high_price, is_test=is_test, offer_id=object_model.id,
        )
    )

    return entities.GetOfferDuplicatesTabsResponse(
        tabs=get_tabs(
            duplicate_count=duplicates_count,
            same_building_count=same_building_count,
            similar_count=similar_count
        ),
    )
