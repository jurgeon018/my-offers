from my_offers import entities, enums
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.services import offer_view
from my_offers.services.duplicates.helpers.auction import load_auction_bets
from my_offers.services.duplicates.helpers.tabs import get_tabs
from my_offers.services.offers import get_page_info, get_pagination, load_object_model


async def v1_get_offer_similars_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesResponse:
    tab_type = request.type if request.type else enums.DuplicateTabType.all

    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    limit, offset = get_pagination(request.pagination)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return _get_empty_response(limit, offset)


    if not object_infos:
        return _get_empty_response(limit, offset)

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


def _get_empty_response(limit: int, offset: int) -> entities.GetOfferDuplicatesResponse:
    return entities.GetOfferDuplicatesResponse(
        offers=[],
        tabs=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )
