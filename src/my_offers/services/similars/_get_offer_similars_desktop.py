from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.services import offer_view
from my_offers.services.auctions import load_auction_bets
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


def _get_empty_response(limit, offset) -> entities.GetOfferDuplicatesDesktopResponse:
    return entities.GetOfferDuplicatesDesktopResponse(
        offers=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )
