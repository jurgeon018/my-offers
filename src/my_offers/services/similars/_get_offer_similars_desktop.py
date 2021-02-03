import asyncio
from typing import Optional, Tuple

from simple_settings import settings

from my_offers import entities, enums
from my_offers.entities.duplicates import DuplicateSubscription
from my_offers.helpers.page_info import get_page_info, get_pagination
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories import postgresql
from my_offers.services import auctions, offer_view
from my_offers.services import offers as offers_module
from my_offers.services.notifications import get_notification_settings
from my_offers.services.similars.helpers.table import get_similar_table_suffix


async def v1_get_offer_similars_desktop_public(
        request: entities.GetOfferDuplicatesDesktopRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesDesktopResponse:
    """ Получить список объявлиний типа 'дубли', 'похожие', 'в этом доме' для конрентного объявления. """
    max_count = settings.MAX_SIMILAR_FOR_DESKTOP if settings.MAX_SIMILAR_FOR_DESKTOP > 0 else 100
    subscription = await get_notification_settings(user_id=realty_user_id)
    limit, offset = _get_pagination(pagination=request.pagination, max_count=max_count)
    if offset >= max_count:
        return _get_empty_response(limit, offset, subscription)

    object_model = await offers_module.load_object_model(user_id=realty_user_id, offer_id=request.offer_id)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return _get_empty_response(limit, offset, subscription)

    suffix = get_similar_table_suffix(object_model)
    # todo: https://jira.cian.tech/browse/CD-85593 - для вкладки ВСЕ общее кол-во можно считать через window функцию
    similars, counter = await asyncio.gather(
        postgresql.get_similars_by_offer_id(
            tab_type=enums.DuplicateTabType.all,
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
        return _get_empty_response(limit, offset, subscription)

    object_models = await postgresql.get_offers_by_ids_keep_order(list(similars.keys()))
    auction_bets = await auctions.load_auction_bets(object_models)

    offers = [
        offer_view.build_duplicate_view_desktop(
            object_model=object_model,
            auction_bets=auction_bets,
            duplicate_type=similars[object_model.id].similar_type,
        )
        for object_model in object_models
    ]

    return entities.GetOfferDuplicatesDesktopResponse(
        subscription=subscription,
        offers=offers,
        page=get_page_info(limit=limit, offset=offset, total=min(counter.total_count, max_count)),
    )


def _get_empty_response(
        limit: int,
        offset: int,
        subscription: DuplicateSubscription
) -> entities.GetOfferDuplicatesDesktopResponse:
    return entities.GetOfferDuplicatesDesktopResponse(
        subscription=subscription,
        offers=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )


def _get_pagination(
        *,
        pagination: Optional[entities.Pagination],
        max_count: int
) -> Tuple[int, int]:
    limit, offset = get_pagination(pagination)

    if limit + offset >= max_count:
        limit = max_count - offset

    return limit, offset
