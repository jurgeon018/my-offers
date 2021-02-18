import datetime
from typing import Any, Dict

from my_offers import entities, enums
from my_offers.entities import AvailableActions
from my_offers.entities.mobile_offer import (
    MobOffer,
    MobPrice,
    OfferAuction,
    OfferComplaint,
    OfferDeactivatedService,
    OfferStats,
)
from my_offers.entities.page_info import MobilePageInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.offers import get_filters_mobile


async def v1_get_my_offers_public(
        request: entities.MobileGetMyOffersRequest,
        realty_user_id: int
) -> entities.MobileGetMyOffersResponse:
    # TODO: CD-100662
    # pylint: disable=unused-variable
    filters: Dict[str, Any] = await get_filters_mobile(
        filters=request.filters,
        user_id=realty_user_id,
        tab_type=request.tab_type,
        search_text=request.search,
    )

    return entities.MobileGetMyOffersResponse(
        page=MobilePageInfo(
            limit=request.limit,
            offset=request.offset,
            can_load_more=False
        ),
        offers=[
            MobOffer(
                offer_id=36298746,
                price=MobPrice(
                    value=9_900_000,
                    currency=Currency.rur,
                ),
                status=Status.published,
                offer_type=enums.OfferType.flat,
                deal_type=enums.DealType.sale,
                category=Category.flat_sale,
                is_archived=False,
                has_video_offence=False,
                has_photo_offence=False,
                is_object_on_premoderation=False,
                identification_pending=False,
                is_auction=True,
                formatted_price='9\xa0900\xa0000₽',
                formatted_info='formatted_info',
                formatted_address='formatted_address',
                description='тестовое описание замоканного объявления',
                available_actions=AvailableActions(
                    can_edit=True,
                    can_restore=True,
                    can_update_edit_date=True,
                    can_move_to_archive=True,
                    can_delete=True,
                    can_raise=True,
                    can_raise_without_addform=True,
                    can_change_publisher=True,
                    can_view_similar_offers=True
                ),
                services=[enums.OfferServices.auction, enums.OfferServices.premium],
                deactivated_service=OfferDeactivatedService(
                    description='description',
                    is_auto_restore_on_payment_enabled=True
                ),
                auction=OfferAuction(
                    increase_bets_positions_count=2,
                    current_bet=5.1,
                    note_bet='note_bet',
                    is_available_auction=True,
                    concurrencyTypes=['concurrencyTypes'],
                    type='type',
                    name='name',
                    is_active=True,
                    is_strategy_enabled=True,
                    is_fixed_bet=False,
                    strategy_description='strategy_description',
                    concurrency_type_title='concurrency_type_title'
                ),
                stats=OfferStats(
                    competitors_count=100,
                    duplicates_count=10,
                    calls_count=999,
                    skipped_calls_count=1,
                    total_views=1111,
                    daily_views=99,
                    favorites=5
                ),
                archived_date=datetime.datetime(2020, 12, 14, 22, 44, 57, 890178, tzinfo=datetime.timezone.utc),
                photo='https://cdn-p.cian.site/images/3/267/099/kvartira-moskva-golubinskaya-ulica-990762376-2.jpg',
                publish_till_date=datetime.datetime(2020, 12, 10, 22, 44, 57, 890178, tzinfo=datetime.timezone.utc),
                complaints=[OfferComplaint(
                    id=1,
                    date=datetime.datetime(2020, 12, 11, 22, 44, 57, 890178, tzinfo=datetime.timezone.utc),
                    comment='comment',
                    reason_text='reason_text',
                    decline=True
                )]
            )
        ]
    )