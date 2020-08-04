import asyncio
from typing import Dict, List

from my_offers import entities, enums
from my_offers.helpers.category import get_types
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.postgresql.offers_duplicates import (
    get_offer_duplicates,
    get_offer_duplicates_ids,
    get_offers_in_same_building,
    get_offers_in_same_building_count,
    get_similar_offers,
    get_similar_offers_count,
)
from my_offers.services import offer_view
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.announcement.fields.is_test import get_is_test
from my_offers.services.auctions import get_auction_bets_degradation_handler
from my_offers.services.duplicates.helpers.range_price import get_range_price
from my_offers.services.duplicates.helpers.rooms_count import get_possible_room_counts
from my_offers.services.duplicates.helpers.tabs import get_tabs
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.services.offers import get_page_info, get_pagination, load_object_model


async def v1_get_offer_duplicates_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesResponse:
    tab_type = request.type if request.type else enums.DuplicateTabType.all

    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    _, deal_type = get_types(object_model.category)
    limit, offset = get_pagination(request.pagination)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return get_empty_response(limit, offset)

    offer_id = object_model.id
    district_id = get_district_id(object_model.geo.district)
    house_id = get_house_id(object_model.geo.address)
    rooms_list = get_possible_room_counts(object_model.rooms_count)
    low_price, high_price = get_range_price(
        bargain_terms=object_model.bargain_terms,
        total_area=object_model.total_area
    )
    is_test = get_is_test(object_model)
    duplicates_ids = await get_offer_duplicates_ids(offer_id)
    duplicates_count = len(duplicates_ids)
    duplicates_ids.append(offer_id)

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

    if tab_type.is_same_building:
        total = same_building_count
        object_infos = await get_offers_in_same_building(
            deal_type=deal_type, house_id=house_id, rooms_counts=rooms_list, low_price=low_price,
            high_price=high_price, duplicates_ids=duplicates_ids, is_test=is_test, limit=limit, offset=offset
        ) if total else []

    elif tab_type.is_similar:
        total = similar_count
        object_infos = await get_similar_offers(
            deal_type=deal_type, district_id=district_id, house_id=house_id, rooms_counts=rooms_list,
            low_price=low_price, high_price=high_price, is_test=is_test, offer_id=offer_id, limit=limit, offset=offset
        ) if total else []

    elif tab_type.is_duplicate:
        total = duplicates_count
        object_infos = await get_offer_duplicates(
            offer_id=offer_id, limit=limit, offset=offset
        ) if total else []

    else:
        # todo https://jira.cian.tech/browse/CD-85593
        object_infos = []
        need_more_offers = False
        limit_for_all = limit
        offset_for_all = offset

        if offset_for_all < duplicates_count:
            duplicates = await get_offer_duplicates(
                offer_id=offer_id, limit=limit_for_all, offset=offset_for_all
            ) if duplicates_count else []
            object_infos.extend(duplicates)
            limit_for_all = limit_for_all - len(duplicates)
            if limit_for_all:
                need_more_offers = True

        if offset_for_all >= duplicates_count or need_more_offers:
            offset_for_all = 0 if need_more_offers else offset_for_all - duplicates_count
            same_building_offers = await get_offers_in_same_building(
                deal_type=deal_type, house_id=house_id, rooms_counts=rooms_list, low_price=low_price,
                high_price=high_price, duplicates_ids=duplicates_ids, is_test=is_test,
                limit=limit_for_all, offset=offset_for_all
            ) if same_building_count else []
            object_infos.extend(same_building_offers)
            limit_for_all = limit_for_all - len(same_building_offers)
            if limit_for_all:
                need_more_offers = True

        duplicates_and_same_building_count = duplicates_count + same_building_count
        if offset_for_all >= duplicates_and_same_building_count or need_more_offers:
            offset_for_all = 0 if need_more_offers else offset_for_all - duplicates_and_same_building_count
            similar_offers = await get_similar_offers(
                deal_type=deal_type, district_id=district_id, house_id=house_id, rooms_counts=rooms_list,
                low_price=low_price, high_price=high_price, is_test=is_test, offer_id=offer_id,
                limit=limit_for_all, offset=offset_for_all,
            ) if similar_count else []
            object_infos.extend(similar_offers)

        total = duplicates_count + same_building_count + similar_count

    if not object_infos:
        return get_empty_response(limit, offset)

    auction_bets = await load_auction_bets([object_info[0] for object_info in object_infos])

    offers = []
    for object_model, duplicate_type in object_infos:
        offers.append(offer_view.build_duplicate_view(
            object_model=object_model,
            auction_bets=auction_bets,
            duplicate_type=duplicate_type,
        ))

    return entities.GetOfferDuplicatesResponse(
        offers=offers,
        tabs=get_tabs(
            duplicate_count=duplicates_count,
            same_building_count=same_building_count,
            similar_count=similar_count
        ),
        page=get_page_info(limit=limit, offset=offset, total=total),
    )


def get_empty_response(limit: int, offset: int) -> entities.GetOfferDuplicatesResponse:
    return entities.GetOfferDuplicatesResponse(
        offers=[],
        tabs=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )


async def load_auction_bets(object_models: List[ObjectModel]) -> Dict[int, int]:
    offer_ids = []
    for object_model in object_models:
        terms = object_model.publish_terms.terms if object_model.publish_terms else None
        if not terms:
            continue

        for term in terms:
            if term.services and Services.auction in term.services:
                offer_ids.append(object_model.id)
                break

    if not offer_ids:
        return {}

    result = await get_auction_bets_degradation_handler(offer_ids)

    return result.value
