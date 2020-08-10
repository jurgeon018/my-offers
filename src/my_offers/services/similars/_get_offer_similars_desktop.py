import asyncio
from typing import List, Optional, Tuple

from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.enums import DealType, DuplicateType
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import is_test
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import ObjectModel
from my_offers.services import offer_view
from my_offers.services.announcement.fields.district_id import get_district_id
from my_offers.services.announcement.fields.house_id import get_house_id
from my_offers.services.duplicates.helpers.auction import load_auction_bets
from my_offers.services.duplicates.helpers.range_price import get_range_price
from my_offers.services.duplicates.helpers.rooms_count import get_possible_room_counts
from my_offers.services.offers import get_page_info, get_pagination, load_object_model


async def v1_get_offer_similars_desktop_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesDesktopResponse:
    """ Получить список объявлиний типа 'дубли', 'похожие', 'в этом доме' для конрентного объявления. """
    if not request.type.is_all:
        raise BrokenRulesException([Error(
            key='type',
            code='type_not_supported',
        )])

    limit, offset = get_pagination(request.pagination)
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    _, deal_type = get_types(object_model.category)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return _get_empty_response(limit, offset)

    offer_id = object_model.id
    district_id = get_district_id(object_model.geo.district)
    house_id = get_house_id(object_model.geo.address)
    rooms_list = get_possible_room_counts(object_model.rooms_count)
    low_price, high_price = get_range_price(
        bargain_terms=object_model.bargain_terms,
        total_area=object_model.total_area
    )
    test = is_test(object_model)
    duplicates_ids = await get_offer_duplicates_ids(offer_id)
    duplicates_count = len(duplicates_ids)
    duplicates_ids.append(offer_id)

    same_building_count, similar_count = await asyncio.gather(
        get_offers_in_same_building_count(
            deal_type=deal_type, house_id=house_id, rooms_counts=rooms_list, low_price=low_price,
            high_price=high_price, duplicates_ids=duplicates_ids, is_test=test,
        ),
        get_similar_offers_count(
            deal_type=deal_type, district_id=district_id, house_id=house_id, rooms_counts=rooms_list,
            low_price=low_price, high_price=high_price, is_test=test, offer_id=object_model.id,
        )
    )

    object_infos, total = await _get_all_duplicates_and_similar(
        offer_id=offer_id,
        duplicates_count=duplicates_count,
        limit=limit,
        offset=offset,
        same_building_count=same_building_count,
        similar_count=similar_count,
        deal_type=deal_type,
        house_id=house_id,
        low_price=low_price,
        high_price=high_price,
        duplicates_ids=duplicates_ids,
        is_test=test,
        district_id=district_id,
        rooms_list=rooms_list
    )

    if not object_infos:
        return _get_empty_response(limit, offset)

    auction_bets = await load_auction_bets([object_info[0] for object_info in object_infos])
    offers = [
        offer_view.build_duplicate_view_desktop(
            object_model=object_model,
            auction_bets=auction_bets,
            duplicate_type=duplicate_type,
        )
        for object_model, duplicate_type in object_infos
    ]

    return entities.GetOfferDuplicatesDesktopResponse(
        offers=offers,
        page=get_page_info(limit=limit, offset=offset, total=total),
    )


async def _get_all_duplicates_and_similar(
        *,
        offer_id: int,
        duplicates_count: int,
        limit: int,
        offset: int,
        same_building_count: int,
        similar_count: int,
        deal_type: DealType,
        house_id: int,
        low_price: float,
        high_price: float,
        duplicates_ids: List[int],
        is_test: bool,
        district_id: Optional[int],
        rooms_list: Optional[Tuple[str, str, str]]
) -> Tuple[List[Tuple[ObjectModel, DuplicateType]], int]:
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

    return object_infos, total


def _get_empty_response(limit, offset) -> entities.GetOfferDuplicatesDesktopResponse:
    return entities.GetOfferDuplicatesDesktopResponse(
        offers=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )
