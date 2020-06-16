import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import pytz
from simple_settings import settings

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.offer_view_model import Subagent
from my_offers.enums import ModerationOffenceStatus
from my_offers.helpers.statsd import async_statsd_timer
from my_offers.repositories.postgresql.agents import get_master_user_id
from my_offers.services.agencies_settings import get_settings_degradation_handler
from my_offers.services.announcement_api import can_update_edit_date_degradation_handler
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls_degradation_handler
from my_offers.services.offers._get_offers import (
    get_agent_names_degradation_handler,
    get_favorites_counts_degradation_handler,
    get_last_import_errors_degradation_handler,
    get_offer_premoderations_degradation_handler,
    get_offers_offence_degradation_handler,
    get_offers_payed_till_degradation_handler,
    get_offers_update_at_degradation_handler,
    get_searches_counts_degradation_handler,
    get_views_counts_degradation_handler,
)
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichData, EnrichItem, EnrichParams, GeoUrlKey
from my_offers.services.search_coverage import get_offers_search_coverage_degradation_handler
from my_offers.services.seo_urls.get_seo_urls import get_query_strings_for_address_degradation_handler


logger = logging.getLogger(__name__)


async def load_enrich_data(
    *,
    params: EnrichParams,
    status_tab: enums.OfferStatusTab
) -> Tuple[EnrichData, Dict[str, bool]]:
    offer_ids = params.get_offer_ids()
    if not offer_ids:
        return EnrichData(
            auctions={},
            jk_urls={},
            geo_urls={},
            can_update_edit_dates={},
            import_errors={},
            favorites_counts={},
            searches_counts={},
            views_counts={},
        ), {}

    enriched = [
        _load_jk_urls(params.get_jk_ids()),
        _load_geo_urls(params.get_geo_url_params()),
        _load_can_update_edit_dates(offer_ids),
        _load_agency_settings(params.get_user_id()),
        _load_subagents(params.get_agent_ids()),
    ]

    if status_tab.is_active:
        enriched.extend([
            _load_favorites_counts(offer_ids),
            _load_searches_counts(offer_ids),
            _load_views_counts(offer_ids),
            _load_auctions(offer_ids),
            _load_payed_till(offer_ids),
        ])
    elif status_tab.is_not_active:
        enriched.extend([
            _load_import_errors(offer_ids),
            _load_premoderation_info(offer_ids),
            _load_archive_date(offer_ids),
        ])

    elif status_tab.is_declined:
        enriched.extend([
            _load_moderation_info(offer_ids),
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


@async_statsd_timer('enrich.load_moderation_info')
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


@async_statsd_timer('enrich.load_coverage')
async def _load_coverage(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_search_coverage_degradation_handler(offer_ids)

    return EnrichItem(key='coverage', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_auctions')
async def _load_auctions(offer_ids: List[int]) -> EnrichItem:
    # todo: https://jira.cian.tech/browse/CD-74479
    return EnrichItem(key='auctions', degraded=False, value={})


@async_statsd_timer('enrich.load_jk_urls')
async def _load_jk_urls(jk_ids: List[int]) -> EnrichItem:
    if not jk_ids:
        return EnrichItem(key='jk_urls', degraded=False, value={})

    result = await get_newbuilding_urls_degradation_handler(jk_ids)

    return EnrichItem(key='jk_urls', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_geo_urls')
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


@async_statsd_timer('enrich.load_can_update_edit_dates')
async def _load_can_update_edit_dates(offer_ids: List[int]) -> EnrichItem:
    result = await can_update_edit_date_degradation_handler(offer_ids)

    return EnrichItem(key='can_update_edit_dates', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_import_errors')
async def _load_import_errors(offer_ids: List[int]) -> EnrichItem:
    result = await get_last_import_errors_degradation_handler(offer_ids)

    return EnrichItem(key='import_errors', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_agency_settings')
async def _load_agency_settings(user_id: int) -> EnrichItem:
    agency_id = await get_master_user_id(user_id)
    if not agency_id:
        return EnrichItem(key='agency_settings', degraded=False, value=None)

    result = await get_settings_degradation_handler(agency_id)

    return EnrichItem(key='agency_settings', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_subagents')
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


@async_statsd_timer('enrich.load_premoderation_info')
async def _load_premoderation_info(offer_ids: List[int]) -> EnrichItem:
    result = await get_offer_premoderations_degradation_handler(offer_ids)

    return EnrichItem(key='premoderation_info', degraded=result.degraded, value=set(result.value))


@async_statsd_timer('enrich.load_archive_date')
async def _load_archive_date(offer_ids: List[int]) -> EnrichItem:
    # todo: CD-77579 Сейчас, по договоренности с продуктом, делаю костыть,
    # исправить в задаче https://jira.cian.tech/browse/CD-77579
    # обсуждение https://cianru.slack.com/archives/CNYSG64UD/p1585559101117800

    result = await get_offers_update_at_degradation_handler(offer_ids)

    return EnrichItem(key='archive_date', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_payed_till')
async def _load_payed_till(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_payed_till_degradation_handler(offer_ids)

    return EnrichItem(key='payed_till', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_views_counts')
async def _load_views_counts(offer_ids: List[int]) -> EnrichItem:
    date_to = datetime.now(tz=pytz.utc)
    date_from = date_to - timedelta(days=settings.DAYS_FOR_STATISTICS)
    result = await get_views_counts_degradation_handler(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    return EnrichItem(key='views_counts', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_searches_counts')
async def _load_searches_counts(offer_ids: List[int]) -> EnrichItem:
    date_to = datetime.now(tz=pytz.utc)
    date_from = date_to - timedelta(days=settings.DAYS_FOR_STATISTICS)
    result = await get_searches_counts_degradation_handler(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )

    return EnrichItem(key='searches_counts', degraded=result.degraded, value=result.value)


@async_statsd_timer('enrich.load_favorites_counts')
async def _load_favorites_counts(offer_ids: List[int]) -> EnrichItem:
    result = await get_favorites_counts_degradation_handler(offer_ids)

    return EnrichItem(key='favorites_counts', degraded=result.degraded, value=result.value)
