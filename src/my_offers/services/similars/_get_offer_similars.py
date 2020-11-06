import asyncio

from simple_settings import settings

from my_offers import entities, enums
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories import postgresql
from my_offers.services import auctions, offer_view
from my_offers.services.offers import get_page_info, get_pagination, load_object_model
from my_offers.services.similars.helpers.table import get_similar_table_suffix
from my_offers.services.similars.helpers.tabs import get_tabs


async def v1_get_offer_similars_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int,
) -> entities.GetOfferDuplicatesResponse:
    tab_type = request.type if request.type else enums.DuplicateTabType.all

    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    limit, offset = get_pagination(request.pagination)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return _get_empty_response(limit, offset)

    suffix = get_similar_table_suffix(object_model)
    # todo: https://jira.cian.tech/browse/CD-85593 - для вкладки ВСЕ общее кол-во можно считать через window функцию
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

    object_models = await postgresql.get_offers_by_ids_keep_order(list(similars.keys()))
    auction_bets = await auctions.load_auction_bets(object_models)

    offers = [
        offer_view.build_duplicate_view(
            object_model=object_model,
            auction_bets=auction_bets,
            similar=similars[object_model.id],
        )
        for object_model in object_models
    ]

    return entities.GetOfferDuplicatesResponse(
        offers=offers,
        tabs=get_tabs(
            duplicate_count=counter.duplicates_count,
            same_building_count=counter.same_building_count,
            similar_count=counter.similar_count,
        ),
        page=get_page_info(limit=limit, offset=offset, total=_get_total_count(tab_type=tab_type, counter=counter)),
    )


def _get_empty_response(limit: int, offset: int) -> entities.GetOfferDuplicatesResponse:
    return entities.GetOfferDuplicatesResponse(
        offers=[],
        tabs=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )


def _get_total_count(*, tab_type: enums.DuplicateTabType, counter: entities.OfferSimilarCounter) -> int:
    if tab_type.is_duplicate:
        return counter.duplicates_count
    if tab_type.is_same_building:
        return counter.same_building_count
    if tab_type.is_similar:
        return counter.similar_count

    return counter.total_count
