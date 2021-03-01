import datetime
from typing import Any, Dict, List

from my_offers import entities, enums
from my_offers.entities.mobile_offer import (
    ConcurrencyType,
    MobOffer,
    MobPrice,
    OfferAuction,
    OfferComplaint,
    OfferDeactivatedService,
    OfferStats,
)
from my_offers.entities.page_info import MobilePageInfo
from my_offers.helpers import get_available_actions, is_archived, is_manual
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.offers import get_filters_mobile
from ...offers.enrich.enrich_data import MobileEnrichData
from ...offers.enrich.load_enrich_data import load_mobile_enrich_data
from ...offers.enrich.prepare_enrich_params import prepare_enrich_params
from ._get_objects_models import get_object_models_with_pagination


async def v1_get_my_offers_public(
        request: entities.MobileGetMyOffersRequest,
        realty_user_id: int
) -> entities.MobileGetMyOffersResponse:
    filters: Dict[str, Any] = await get_filters_mobile(
        filters=request.filters,
        user_id=realty_user_id,
        tab_type=request.tab_type,
        search_text=request.search,
    )

    object_models: List[ObjectModel]
    can_load_more: bool
    object_models, can_load_more = await get_object_models_with_pagination(
        filters=filters,
        limit=request.limit,
        offset=request.offset,
        sort_type=request.sort or enums.MobOffersSortType.update_date,
    )

    offers = await _prepare_offers(user_id=realty_user_id, object_models=object_models, tab_type=request.tab_type)

    return entities.MobileGetMyOffersResponse(
        page=MobilePageInfo(
            limit=request.limit,
            offset=request.offset,
            can_load_more=can_load_more
        ),
        offers=offers
    )


async def _prepare_offers(
        *,
        user_id: int,
        object_models: List[ObjectModel],
        tab_type: enums.MobTabType,
) -> List[MobOffer]:
    # получение данных для обогащения
    enrich_params = prepare_enrich_params(models=object_models, user_id=user_id)
    enrich_data = await load_mobile_enrich_data(params=enrich_params, tab_type=tab_type)

    return [
        _prepare_offer(object_model=object_model, enrich_data=enrich_data)
        for object_model in object_models
    ]


def _prepare_offer(*, object_model: ObjectModel, enrich_data: MobileEnrichData) -> MobOffer:
    offer_id = object_model.id
    manual = is_manual(object_model.source)
    archived = is_archived(object_model.flags)
    force_raise = bool(
        enrich_data.get_duplicates_counts(offer_id)
        or enrich_data.get_same_building_counts(offer_id)
    )
    agent_hierarchy_data = enrich_data.agent_hierarchy_data

    return MobOffer(
        offer_id=36298746,
        price=MobPrice(
            value=9_900_000,
            currency=Currency.rur,
        ),
        status=enums.MobStatus.published,
        offer_type=enums.OfferType.flat,
        deal_type=enums.DealType.sale,
        category=Category.flat_sale,
        is_archived=False,
        has_video_offence=offer_id in enrich_data.video_offences,
        has_photo_offence=offer_id in enrich_data.image_offences,
        is_object_on_premoderation=False,
        identification_pending=False,
        is_auction=True,
        formatted_price='9\xa0900\xa0000₽',
        formatted_info='formatted_info',
        formatted_address='formatted_address',
        description='тестовое описание замоканного объявления',
        available_actions=get_available_actions(
            status=object_model.status,
            is_archived=archived,
            is_manual=manual,
            can_update_edit_date=enrich_data.can_update_edit_dates.get(offer_id, False),
            agency_settings=enrich_data.agency_settings,
            is_in_hidden_base=object_model.is_in_hidden_base,
            agent_hierarchy_data=agent_hierarchy_data,
            force_raise=force_raise,
            can_view_similar_offers=is_offer_for_similar(
                status=object_model.status,
                category=object_model.category
            ),
            payed_by=enrich_data.offers_payed_by.get(offer_id)
        ),
        services=[Services.auction, Services.premium],
        deactivated_service=OfferDeactivatedService(
            description='description',
            is_auto_restore_on_payment_enabled=True
        ),
        auction=OfferAuction(
            increase_bets_positions_count=2,
            current_bet=5.1,
            note_bet='note_bet',
            is_available_auction=True,
            concurrency_types=[ConcurrencyType(
                type='type',
                name='name',
                is_active=True
            )],
            is_strategy_enabled=True,
            is_fixed_bet=False,
            strategy_description='strategy_description',
            concurrency_type_title='concurrency_type_title'
        ),
        stats=OfferStats(
            competitors_count=enrich_data.get_same_building_counts(offer_id),
            duplicates_count=enrich_data.get_duplicates_counts(offer_id),
            calls_count=999,
            skipped_calls_count=1,
            total_views=enrich_data.views_counts.get(offer_id),
            daily_views=99,
            favorites=enrich_data.favorites_counts.get(offer_id),
        ),
        archived_date=datetime.datetime(2020, 12, 14, 22, 44, 57, 890178, tzinfo=datetime.timezone.utc),
        photo='https://cdn-p.cian.site/images/3/267/099/kvartira-moskva-golubinskaya-ulica-990762376-2.jpg',
        publish_till_date=datetime.datetime(2020, 12, 10, 22, 44, 57, 890178, tzinfo=datetime.timezone.utc),
        complaints=[OfferComplaint(
            id=1,
            date=datetime.datetime(2020, 12, 11, 22, 44, 57, 890178, tzinfo=datetime.timezone.utc),
            comment='comment',
        )],
        coworking_id=123,
        is_private_agent=True,
    )
