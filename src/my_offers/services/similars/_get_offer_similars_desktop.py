import asyncio

from cian_web.exceptions import BrokenRulesException, Error
from simple_settings import settings

from my_offers import entities
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories import postgresql
from my_offers.services import auctions, offer_view
from my_offers.services.offers import get_page_info, get_pagination, load_object_model
from my_offers.services.similars.helpers.table import get_similar_table_suffix


async def v1_get_offer_similars_desktop_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesDesktopResponse:
    """ Получить список объявлиний типа 'дубли', 'похожие', 'в этом доме' для конрентного объявления. """
    tab_type = request.type
    if not tab_type.is_all:
        raise BrokenRulesException([Error(
            key='type',
            code='type_not_supported',
        )])

    limit, offset = get_pagination(request.pagination)
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return _get_empty_response(limit, offset)

    suffix = get_similar_table_suffix(object_model)
    similars, counter = await asyncio.gather(
        postgresql.get_similars_by_offer_id(
            tab_type=tab_type,
            offer_id=object_model.id,
            limit=limit,
            offset=offset,
            price_kf=settings.SIMILAR_PRICE_KF,
            room_delta=settings.SIMILAR_ROOM_DELTA,
            suffix=suffix
        ),
        postgresql.get_similar_counter_by_offer_id(
            offer_id=object_model.id,
            price_kf=settings.SIMILAR_PRICE_KF,
            room_delta=settings.SIMILAR_ROOM_DELTA,
            suffix=suffix,
        ),
    )

    if not similars:
        return _get_empty_response(limit, offset)

    object_models = await postgresql.get_offers_by_ids(list(similars.keys()))
    auction_bets = await auctions.load_auction_bets(object_models)

    offers = [
        offer_view.build_duplicate_view_desktop(
            object_model=object_model,
            auction_bets=auction_bets,
            duplicate_type=similars[object_model.id],
        )
        for object_model in object_models
    ]

    return entities.GetOfferDuplicatesDesktopResponse(
        offers=offers,
        page=get_page_info(limit=limit, offset=offset, total=counter.total_count),
    )


def _get_empty_response(limit, offset) -> entities.GetOfferDuplicatesDesktopResponse:
    return entities.GetOfferDuplicatesDesktopResponse(
        offers=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )
