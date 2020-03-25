import asyncio
from typing import Dict, List, Optional, Tuple

from my_offers.entities.enrich import AddressUrlParams
from my_offers.enums import ModerationOffenceStatus
from my_offers.repositories import postgresql
from my_offers.repositories.postgresql.agents import get_agent_names, get_master_user_id
from my_offers.repositories.postgresql.offer_import_error import get_last_import_errors
from my_offers.services.agencies_settings import get_settings_degradation_handler
from my_offers.services.announcement_api import can_update_edit_date_degradation_handler
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls_degradation_handler
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichData, EnrichItem, EnrichParams, GeoUrlKey
from my_offers.services.search_coverage import get_offers_search_coverage_degradation_handler
from my_offers.services.seo_urls.get_seo_urls import get_query_strings_for_address_degradation_handler


async def load_enrich_data(params: EnrichParams) -> Tuple[EnrichData, Dict[str, bool]]:
    offer_ids = params.get_offer_ids()
    if not offer_ids:
        return EnrichData(
            coverage={},
            auctions={},
            jk_urls={},
            geo_urls={},
            can_update_edit_dates={},
            import_errors={},
        ), {}

    data = await asyncio.gather(
        _load_coverage(offer_ids),
        _load_auctions(offer_ids),
        _load_jk_urls(params.get_jk_ids()),
        _load_geo_urls(params.get_geo_url_params()),
        _load_can_update_edit_dates(offer_ids),
        _load_import_errors(offer_ids),
        _load_moderation_info(offer_ids),
        _load_agency_settings(params.get_user_id()),
        _load_agent_names(params.get_agent_ids()),
        # todo: https://jira.cian.tech/browse/CD-75737 Разные обогощения в зависимости от вкладок
    )

    params = {}
    degradation = {}
    for item in data:
        params[item.key] = item.value
        degradation[item.key] = item.degraded

    return EnrichData(**params), degradation


async def _load_moderation_info(offer_ids: List[int]) -> EnrichItem:
    result = await postgresql.get_offers_offence(
        offer_ids=offer_ids,
        status=ModerationOffenceStatus.confirmed
    )
    values = {
        offer_offence.offer_id: offer_offence
        for offer_offence in result
    }

    return EnrichItem(key='moderation_info', degraded=False, value=values)


async def _load_coverage(offer_ids: List[int]) -> EnrichItem:
    result = await get_offers_search_coverage_degradation_handler(offer_ids)

    return EnrichItem(key='coverage', degraded=result.degraded, value=result.value)


async def _load_auctions(offer_ids: List[int]) -> EnrichItem:
    # todo: https://jira.cian.tech/browse/CD-74479
    return EnrichItem(key='auctions', degraded=False, value={})


async def _load_jk_urls(jk_ids: List[int]) -> EnrichItem:
    if not jk_ids:
        return EnrichItem(key='jk_urls', degraded=False, value={})

    result = await get_newbuilding_urls_degradation_handler(jk_ids)

    return EnrichItem(key='jk_urls', degraded=result.degraded, value=result.value)


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


async def _load_can_update_edit_dates(offer_ids: List[int]) -> EnrichItem:
    result = await can_update_edit_date_degradation_handler(offer_ids)

    return EnrichItem(key='can_update_edit_dates', degraded=result.degraded, value=result.value)


async def _load_import_errors(offer_ids: List[int]) -> EnrichItem:
    result = await get_last_import_errors(offer_ids)

    return EnrichItem(key='import_errors', degraded=False, value=result)


async def _load_agency_settings(user_id: int) -> EnrichItem:
    agency_id = await get_master_user_id(user_id)
    if not agency_id:
        return EnrichItem(key='agency_settings', degraded=False, value=None)

    result = await get_settings_degradation_handler(agency_id)

    return EnrichItem(key='agency_settings', degraded=result.degraded, value=result.value)


async def _load_agent_names(user_ids: [List[int]]) -> EnrichItem:
    if not user_ids:
        return EnrichItem(key='agent_names', degraded=False, value=None)

    data = await get_agent_names(user_ids)

    result = {}
    for item in data:
        name = item.get_name()
        if not name:
            continue

        result[item.id] = name

    return EnrichItem(key='agent_names', degraded=False, value=result)
