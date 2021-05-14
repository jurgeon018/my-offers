import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import pytz
from cian_core.degradation import DegradationResult
from cian_core.statsd import statsd_timer
from simple_settings import settings

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.mobile_offer import ConcurrencyType, OfferAuction, OfferComplaint
from my_offers.entities.offer_view_model import Subagent
from my_offers.enums import DuplicateTabType, ModerationOffenceStatus
from my_offers.repositories.auction.entities import MobileBetAnnouncementInfo, V1GetAnnouncementsInfoForMobile
from my_offers.repositories.callbook.entities import OfferCallCount
from my_offers.repositories.moderation_checks_orchestrator.entities import UserIdentificationResult
from my_offers.repositories.postgresql.agents import get_master_user_id
from my_offers.services import favorites
from my_offers.services.agencies_settings import get_settings_degradation_handler
from my_offers.services.announcement_api import can_update_edit_date_degradation_handler
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls_degradation_handler
from my_offers.services.offences import (
    get_offers_with_image_offences_degradation_handler,
    get_offers_with_video_offences_degradation_handler,
)
from my_offers.services.offer_relevance_warnings import get_offer_relevance_warnings_degradation_handler
from my_offers.services.offers._degradation_handlers import (
    get_agent_hierarchy_data_degradation_handler,
    get_agent_names_degradation_handler,
    get_auctions_mobile_degradation_handler,
    get_calls_count_degradation_handler,
    get_deactivated_services_degradation_handler,
    get_favorites_counts_degradation_handler,
    get_last_import_errors_degradation_handler,
    get_offer_premoderations_degradation_handler,
    get_offers_offence_degradation_handler,
    get_offers_payed_by_degradation_handler,
    get_offers_payed_till_excluding_calltracking_degradation_handler,
    get_offers_update_at_degradation_handler,
    get_offers_with_pending_identification_handler,
    get_searches_counts_degradation_handler,
    get_similars_counters_by_offer_ids_degradation_handler,
    get_views_counts_degradation_handler,
    get_views_current_degradation_handler,
    get_views_total_degradation_handler,
)
from my_offers.services.offers.enrich.enrich_data import (
    AddressUrls,
    EnrichData,
    EnrichItem,
    EnrichParams,
    GeoUrlKey,
    MobileEnrichData,
)
from my_offers.services.search_coverage import get_offers_search_coverage_degradation_handler
from my_offers.services.seo_urls.get_seo_urls import get_query_strings_for_address_degradation_handler
from my_offers.services.similars.helpers.table import get_similar_table_suffix_by_params


logger = logging.getLogger(__name__)


async def load_mobile_enrich_data(
        *,
        params: EnrichParams,
        tab_type: enums.MobTabType,
) -> MobileEnrichData:
    """ Загружает данные из внешних источников для разных типов вкладок. """
    offer_ids = params.get_offer_ids()
    user_id = params.get_user_id()
    if not offer_ids:
        return MobileEnrichData(
            agent_hierarchy_data=(await get_agent_hierarchy_data_degradation_handler(params.get_user_id())).value
        )

    is_active = tab_type.is_rent or tab_type.is_sale

    enriched = [
        asyncio.ensure_future(_load_agent_hierarchy_data(user_id)),
        asyncio.ensure_future(_load_can_update_edit_dates(
            offer_ids=offer_ids,
            status_tab=enums.OfferStatusTab.active if is_active else enums.OfferStatusTab.archived
        )),
        asyncio.ensure_future(_load_agency_settings(user_id)),
        asyncio.ensure_future(_load_offers_payed_by(offer_ids)),
        asyncio.ensure_future(_load_deactivated_service(user_id, offer_ids)),
    ]

    if is_active:
        enriched.extend([
            asyncio.ensure_future(_load_favorites_counts(offer_ids)),
            asyncio.ensure_future(_load_views_totals_counts(offer_ids)),
            asyncio.ensure_future(_load_views_daily_counts(offer_ids)),
            asyncio.ensure_future(_load_calls(offer_ids)),
            asyncio.ensure_future(_load_payed_till(offer_ids)),
            asyncio.ensure_future(_load_mobile_auctions(offer_ids, params.get_user_id())),
            asyncio.ensure_future(_load_pending_identification_offers([params.get_user_id()])),
            asyncio.ensure_future(_load_offers_similars_counters(
                offer_ids=params.get_similar_offers(),
                is_test=params.is_test_offers
            )),
        ])
    else:
        enriched.extend([
            asyncio.ensure_future(_load_video_offenses(offer_ids)),
            asyncio.ensure_future(_load_image_offenses(offer_ids)),
            asyncio.ensure_future(_load_moderation_mobile_info(offer_ids)),
            asyncio.ensure_future(_load_premoderation_info(offer_ids)),
        ])

    data = await asyncio.gather(*enriched)

    loaded_data = {}
    for item in data:
        loaded_data[item.key] = item.value

    return MobileEnrichData(**loaded_data)


async def load_enrich_data(
        *,
        params: EnrichParams,
        status_tab: enums.OfferStatusTab
) -> Tuple[EnrichData, Dict[str, bool]]:
    """ Загружает данные из внешних источников для разных типов вкладок. """
    offer_ids = params.get_offer_ids()
    if not offer_ids:
        return EnrichData(
            agent_hierarchy_data=(await get_agent_hierarchy_data_degradation_handler(params.get_user_id())).value
        ), {}

    enriched = [
        asyncio.ensure_future(_load_agent_hierarchy_data(params.get_user_id())),
        asyncio.ensure_future(_load_can_update_edit_dates(offer_ids=offer_ids, status_tab=status_tab)),
        asyncio.ensure_future(_load_agency_settings(params.get_user_id())),
        asyncio.ensure_future(_load_offers_payed_by(offer_ids)),
        asyncio.ensure_future(_load_jk_urls(params.get_jk_ids())),
        asyncio.ensure_future(_load_geo_urls(params.get_geo_url_params())),
        asyncio.ensure_future(_load_subagents(params.get_agent_ids())),

    ]

    if status_tab.is_active:
        enriched.extend([
            asyncio.ensure_future(_load_favorites_counts(offer_ids)),
            asyncio.ensure_future(_load_searches_counts(offer_ids)),
            asyncio.ensure_future(_load_views_counts(offer_ids)),
            asyncio.ensure_future(_load_calls(offer_ids)),
            asyncio.ensure_future(_load_auctions(offer_ids)),
            asyncio.ensure_future(_load_payed_till(offer_ids)),
            asyncio.ensure_future(_load_offers_similars_counters(
                offer_ids=params.get_similar_offers(),
                is_test=params.is_test_offers
            )),
            asyncio.ensure_future(_load_offer_relevance_warnings(offer_ids)),

        ])
    elif status_tab.is_not_active:
        enriched.extend([
            asyncio.ensure_future(_load_import_errors(offer_ids)),
            asyncio.ensure_future(_load_premoderation_info(offer_ids)),
            asyncio.ensure_future(_load_archive_date(offer_ids)),
        ])
    elif status_tab.is_declined:
        enriched.extend([
            asyncio.ensure_future(_load_moderation_info(offer_ids)),
        ])
    elif status_tab.is_archived:
        # не требуется доп. обогащений
        pass
    elif status_tab.is_deleted:
        # не требуется доп. обогащений
        pass
    else:
        logger.warning('Unsupported status tab: %s', status_tab)

    data = await asyncio.gather(*enriched)

    loaded_data = {}
    degradation = {}
    for item in data:
        loaded_data[item.key] = item.value
        degradation[item.key] = item.degraded

    return EnrichData(**loaded_data), degradation


@statsd_timer(key='enrich.load_moderation_info')
async def _load_moderation_info(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_offence_degradation_handler(
        offer_ids=offer_ids,
        status=ModerationOffenceStatus.confirmed
    )
    values = {
        offer_offence.offer_id: offer_offence
        for offer_offence in result.value
    }

    return EnrichItem(key='moderation_info', degraded=result.degraded, value=values)


@statsd_timer(key='enrich.load_moderation_mobile_info')
async def _load_moderation_mobile_info(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_offence_degradation_handler(
        offer_ids=offer_ids,
        status=ModerationOffenceStatus.confirmed
    )
    values = {}

    for offence_item in result.value:
        complaint = OfferComplaint(
            id=offence_item.offence_id,
            date=offence_item.created_date,
            comment=offence_item.offence_text,
        )
        if offence_item.offer_id not in values:
            values[offence_item.offer_id] = [complaint]
        else:
            values[offence_item.offer_id].append(complaint)

    return EnrichItem(key='moderation_info', degraded=result.degraded, value=values)


@statsd_timer(key='enrich.load_moderation_mobile_info')
async def _load_pending_identification_offers(user_ids: List[int]) -> EnrichItem:
    result = await get_offers_with_pending_identification_handler(user_ids)
    if result.degraded:
        return EnrichItem(key='offer_with_pending_identification', degraded=result.degraded, value=result.value)

    data: List[UserIdentificationResult] = result.value

    values = set()

    for pending_result in data:
        if pending_result.object_ids:
            values.update(pending_result.object_ids)

    return EnrichItem(key='offer_with_pending_identification', degraded=result.degraded, value=values)


@statsd_timer(key='enrich.load_coverage')
async def _load_coverage(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_search_coverage_degradation_handler(offer_ids)

    return EnrichItem(key='coverage', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_auctions')
async def _load_auctions(offer_ids: List[int]) -> EnrichItem:
    # todo: https://jira.cian.tech/browse/CD-74479
    return EnrichItem(key='auctions', degraded=False, value={})


@statsd_timer(key='enrich.load_mobile_auctions')
async def _load_mobile_auctions(offer_ids: List[int], user_id: int) -> EnrichItem:
    result: DegradationResult = await get_auctions_mobile_degradation_handler(V1GetAnnouncementsInfoForMobile(
        announcement_ids=offer_ids,
        user_id=user_id,
    ))
    if result.degraded:
        return EnrichItem(key='auctions', degraded=result.degraded, value=result.value)

    data: List[MobileBetAnnouncementInfo] = result.value.announcements

    values: Dict[int, OfferAuction] = {}

    for auction_item in data:
        concurrency_types: List[ConcurrencyType] = []

        for ct in auction_item.concurrency_types:
            concurrency_types.append(ConcurrencyType(
                is_active=ct.is_active,
                name=ct.name,
                type=ct.type.value
            ))

        auction: OfferAuction = OfferAuction(
            increase_bets_positions_count=auction_item.increase_bets_positions_count,
            current_bet=auction_item.current_bet,
            note_bet=auction_item.note_bet,
            is_available_auction=auction_item.is_available_auction,
            concurrency_types=concurrency_types,
            is_strategy_enabled=auction_item.is_strategy_enabled,
            is_fixed_bet=auction_item.is_fixed_bet,
            strategy_description=auction_item.strategy_description,
            concurrency_type_title=auction_item.concurrency_type_title,
        )
        values[auction_item.announcement_id] = auction

    return EnrichItem(key='auctions', degraded=False, value=values)


@statsd_timer(key='enrich.load_jk_urls')
async def _load_jk_urls(jk_ids: List[int]) -> EnrichItem:
    if not jk_ids:
        return EnrichItem(key='jk_urls', degraded=False, value={})

    result = await get_newbuilding_urls_degradation_handler(jk_ids)

    return EnrichItem(key='jk_urls', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_agent_hierarchy_data')
async def _load_agent_hierarchy_data(user_id: int) -> EnrichItem:
    result = await get_agent_hierarchy_data_degradation_handler(user_id)

    return EnrichItem(key='agent_hierarchy_data', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_geo_urls')
async def _load_geo_urls(params: List[AddressUrlParams]) -> EnrichItem:
    result: Dict[GeoUrlKey, AddressUrls] = {}
    degraded = False
    for param in params:
        data = await get_query_strings_for_address_degradation_handler(
            address_elements=param.address_info,
            deal_type=param.deal_type,
            offer_type=param.offer_type,
        )

        if data.degraded:
            degraded = True
            continue

        for i, address in enumerate(param.address_info):
            key = GeoUrlKey(param.deal_type, param.offer_type)
            if key not in result:
                result[key] = AddressUrls()
            result[key].add_url(address=address, url=data.value[i])

    return EnrichItem(key='geo_urls', degraded=degraded, value=result)


@statsd_timer(key='enrich.load_can_update_edit_dates')
async def _load_can_update_edit_dates(offer_ids: List[int], status_tab: enums.OfferStatusTab) -> EnrichItem:
    if not (status_tab.is_active or status_tab.is_not_active):
        return EnrichItem(key='can_update_edit_dates', degraded=False, value=dict.fromkeys(offer_ids, False))

    result = await can_update_edit_date_degradation_handler(offer_ids)

    return EnrichItem(key='can_update_edit_dates', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_import_errors')
async def _load_import_errors(offer_ids: List[int]) -> EnrichItem:
    result = await get_last_import_errors_degradation_handler(offer_ids)

    return EnrichItem(key='import_errors', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_agency_settings')
async def _load_agency_settings(user_id: int) -> EnrichItem:
    agency_id = await get_master_user_id(user_id)
    if not agency_id:
        return EnrichItem(key='agency_settings', degraded=False, value=None)

    result = await get_settings_degradation_handler(agency_id)

    return EnrichItem(key='agency_settings', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_subagents')
async def _load_subagents(user_ids: List[int]) -> EnrichItem:
    if not user_ids:
        return EnrichItem(key='subagents', degraded=False, value=None)

    data = await get_agent_names_degradation_handler(user_ids)

    result = {}
    for item in data.value:
        name = item.get_name()
        if not name:
            continue

        result[item.id] = Subagent(id=item.id, name=name)

    return EnrichItem(key='subagents', degraded=data.degraded, value=result)


@statsd_timer(key='enrich.load_premoderation_info')
async def _load_premoderation_info(offer_ids: List[int]) -> EnrichItem:
    result = await get_offer_premoderations_degradation_handler(offer_ids)

    return EnrichItem(key='premoderation_info', degraded=result.degraded, value=set(result.value))


@statsd_timer(key='enrich.load_archive_date')
async def _load_archive_date(offer_ids: List[int]) -> EnrichItem:
    # todo: CD-77579 Сейчас, по договоренности с продуктом, делаю костыть,
    # исправить в задаче https://jira.cian.tech/browse/CD-77579
    # обсуждение https://cianru.slack.com/archives/CNYSG64UD/p1585559101117800

    result = await get_offers_update_at_degradation_handler(offer_ids)

    return EnrichItem(key='archive_date', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_payed_till')
async def _load_payed_till(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_payed_till_excluding_calltracking_degradation_handler(offer_ids)

    return EnrichItem(key='payed_till', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_views_counts')
async def _load_views_counts(offer_ids: List[int]) -> EnrichItem:
    date_to = datetime.now(tz=pytz.utc)
    date_from = date_to - timedelta(days=settings.DAYS_FOR_STATISTICS)
    result = await get_views_counts_degradation_handler(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    return EnrichItem(key='views_counts', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_views_daily_counts')
async def _load_views_daily_counts(offer_ids: List[int]) -> EnrichItem:
    result = await get_views_current_degradation_handler(
        offer_ids=offer_ids,
        date=datetime.now(tz=pytz.utc),
    )

    return EnrichItem(key='views_daily_counts', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_views_totals')
async def _load_views_totals_counts(offer_ids: List[int]) -> EnrichItem:
    result = await get_views_total_degradation_handler(
        offer_ids=offer_ids,
        date=datetime.now(tz=pytz.utc) - timedelta(days=1),
    )

    return EnrichItem(key='views_totals_counts', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_searches_counts')
async def _load_searches_counts(offer_ids: List[int]) -> EnrichItem:
    date_to = datetime.now(tz=pytz.utc)
    date_from = date_to - timedelta(days=settings.DAYS_FOR_STATISTICS)
    result = await get_searches_counts_degradation_handler(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    return EnrichItem(key='searches_counts', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_favorites_counts')
async def _load_favorites_counts(offer_ids: List[int]) -> EnrichItem:
    if settings.FAVORITES_FROM_MCS:
        result = await favorites.get_favorites_counts_degradation_handler(offer_ids)
    else:
        result = await get_favorites_counts_degradation_handler(offer_ids)

    return EnrichItem(key='favorites_counts', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_similars_counters')
async def _load_offers_similars_counters(*, offer_ids: List[int], is_test: bool) -> EnrichItem:
    if not offer_ids:
        return EnrichItem(key='offers_similars_counts', degraded=False, value={})

    suffix = get_similar_table_suffix_by_params(is_test=is_test)
    result = await get_similars_counters_by_offer_ids_degradation_handler(
        offer_ids=offer_ids,
        price_kf=settings.SIMILAR_PRICE_KF,
        room_delta=settings.SIMILAR_ROOM_DELTA,
        suffix=suffix,
        tab_type=DuplicateTabType.all
    )

    if result.degraded:
        return EnrichItem(key='offers_similars_counts', degraded=result.degraded, value={})

    value = {
        DuplicateTabType.duplicate: {c.offer_id: c.duplicates_count for c in result.value},
        DuplicateTabType.same_building: {c.offer_id: c.same_building_count for c in result.value}
    }
    return EnrichItem(key='offers_similars_counts', degraded=False, value=value)


@statsd_timer(key='enrich.load_offers_payed_by')
async def _load_offers_payed_by(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_payed_by_degradation_handler(offer_ids)

    return EnrichItem(key='offers_payed_by', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_offer_relevance_warnings')
async def _load_offer_relevance_warnings(offer_ids: List[int]) -> EnrichItem:
    result = await get_offer_relevance_warnings_degradation_handler(offer_ids)

    return EnrichItem(key='offer_relevance_warnings', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_video_offenses')
async def _load_video_offenses(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_with_video_offences_degradation_handler(offer_ids)

    return EnrichItem(key='video_offences', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_image_offenses')
async def _load_image_offenses(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_with_image_offences_degradation_handler(offer_ids)

    return EnrichItem(key='image_offences', degraded=result.degraded, value=result.value)


@statsd_timer(key='enrich.load_calls')
async def _load_calls(offer_ids: List[int]) -> EnrichItem:
    result = await get_calls_count_degradation_handler(offer_ids)
    if result.degraded:
        return EnrichItem(key='calls_count', degraded=result.degraded, value={})

    data: List[OfferCallCount] = result.value.data
    return EnrichItem(key='calls_count', degraded=result.degraded, value={item.offer_id: item for item in data})


@statsd_timer(key='enrich.deactivated_service')
async def _load_deactivated_service(user_id: int, offer_ids: List[int]) -> EnrichItem:
    result = await get_deactivated_services_degradation_handler(user_id, offer_ids)
    return EnrichItem(key='deactivated_service', degraded=result.degraded, value=result.value)
