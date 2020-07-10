from typing import Dict, List, Optional, Tuple

from my_offers import entities, enums
from my_offers.enums import DealType, DuplicateType
from my_offers.helpers.category import get_types
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, ObjectModel, Status
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.postgresql.offers_duplicates import (
    get_offer_duplicates,
    get_offer_duplicates_ids,
    get_offers_in_same_building,
    get_similar_offers,
)
from my_offers.services import offer_view
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.announcement.fields.is_test import get_is_test
from my_offers.services.auctions import get_auction_bets_degradation_handler
from my_offers.services.duplicates.helpers.range_price import get_range_price
from my_offers.services.duplicates.helpers.rooms_count import get_possible_room_counts
from my_offers.services.duplicates.helpers.tabs import get_tabs
from my_offers.services.duplicates.helpers.validation_offer import validate_offer
from my_offers.services.offers import get_page_info, get_pagination, load_object_model


async def v1_get_offer_duplicates_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesResponse:
    tab_type = request.type
    if not tab_type:
        tab_type = enums.DuplicateTabType.all
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    _, deal_type = get_types(object_model.category)
    limit, offset = get_pagination(request.pagination)
    offer_id = object_model.id

    if not validate_offer(status=object_model.status, category=object_model.category):
        return get_empty_response(limit, offset)

    if tab_type.is_same_building:
        object_infos, total = await get_data_about_offers_in_same_building(
            object_model=object_model,
            deal_type=deal_type,
            limit=limit,
            offset=offset,
        )
    elif tab_type.is_similar:
        object_infos, total = await get_data_about_similar_offers(
            object_model=object_model,
            deal_type=deal_type,
            limit=limit,
            offset=offset,
        )
    elif tab_type.is_duplicate:
        object_infos, total = await get_data_about_offer_duplicates(
            offer_id=offer_id,
            limit=limit,
            offset=offset,
        )
    else:
        duplicate_obj_mdls, duplicate_total = await get_data_about_offer_duplicates(
            offer_id=offer_id,
        )
        same_buiding_obj_mdls, same_buiding_total = await get_data_about_offers_in_same_building(
            object_model=object_model,
            deal_type=deal_type,
        )
        similar_obj_mdls, similar_total = await get_data_about_similar_offers(
            object_model=object_model,
            deal_type=deal_type,
        )
        object_infos = duplicate_obj_mdls + same_buiding_obj_mdls + similar_obj_mdls
        object_infos = object_infos[offset: offset+limit]
        total = duplicate_total + same_buiding_total + similar_total

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
        tabs=get_tabs(total),
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


async def get_data_about_offer_duplicates(
        *,
        offer_id: int,
        limit: Optional[int] = None,
        offset: int = 0
) -> Tuple[List[Tuple[ObjectModel, DuplicateType]], int]:
    objects_models, total = await get_offer_duplicates(
        offer_id=offer_id,
        limit=limit,
        offset=offset,
    )
    return get_object_models_with_duplicate_type(
        object_models=objects_models,
        duplicate_type=DuplicateType.duplicate
    ), total


async def get_data_about_offers_in_same_building(
        *,
        object_model: ObjectModel,
        deal_type: DealType,
        limit: Optional[int] = None,
        offset: int = 0,
) -> Tuple[List[Tuple[ObjectModel, DuplicateType]], int]:
    house_id = get_house_id(object_model.geo.address)
    duplicates_ids = await get_offer_duplicates_ids(object_model.id)
    duplicates_ids.append(object_model.id)
    rooms_list = get_possible_room_counts(object_model.rooms_count)
    low_price, high_price = get_range_price(
        bargain_terms=object_model.bargain_terms,
        total_area=object_model.total_area,
    )

    if not (house_id and rooms_list and low_price and high_price):
        return [], 0

    objects_models, total = await get_offers_in_same_building(
        deal_type=deal_type,
        house_id=house_id,
        rooms_counts=rooms_list,
        low_price=low_price,
        high_price=high_price,
        duplicates_ids=duplicates_ids,
        is_test=get_is_test(object_model),
        limit=limit,
        offset=offset,
    )

    return get_object_models_with_duplicate_type(
        object_models=objects_models,
        duplicate_type=DuplicateType.same_building
    ), total


async def get_data_about_similar_offers(
        *,
        object_model: ObjectModel,
        deal_type: DealType,
        limit: Optional[int] = None,
        offset: int = 0,
) -> Tuple[List[Tuple[ObjectModel, DuplicateType]], int]:
    district_id = get_district_id(object_model.geo.district)
    house_id = get_house_id(object_model.geo.address)
    rooms_list = get_possible_room_counts(object_model.rooms_count)
    low_price, high_price = get_range_price(
        bargain_terms=object_model.bargain_terms,
        total_area=object_model.total_area,
    )

    if not (district_id and rooms_list and low_price and high_price):
        return [], 0

    objects_models, total = await get_similar_offers(
        deal_type=deal_type,
        district_id=district_id,
        house_id=house_id,
        rooms_counts=rooms_list,
        low_price=low_price,
        high_price=high_price,
        is_test=get_is_test(object_model),
        offer_id=object_model.id,
        limit=limit,
        offset=offset,
    )

    return get_object_models_with_duplicate_type(
        object_models=objects_models,
        duplicate_type=DuplicateType.similar
    ), total


def get_object_models_with_duplicate_type(
        *,
        object_models: List[ObjectModel],
        duplicate_type: DuplicateType,
) -> List[Tuple[ObjectModel, DuplicateType]]:
    offers_info = []
    for object_model in object_models:
        offers_info.append(
            (
                object_model,
                duplicate_type
            )
        )

    return offers_info
