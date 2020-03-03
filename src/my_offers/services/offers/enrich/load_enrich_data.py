import asyncio
from typing import Dict, List, Tuple

from my_offers.entities.enrich import AddressUrlParams
from my_offers.services.announcement.announcement_api import can_update_edit_date_degradation_handler
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls_degradation_handler
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichData, EnrichItem, EnrichParams, GeoUrlKey
from my_offers.services.seo_urls.get_seo_urls import get_query_strings_for_address_degradation_handler


async def load_enrich_data(params: EnrichParams) -> Tuple[EnrichData, Dict[str, bool]]:
    offer_ids = params.get_offer_ids()
    if not offer_ids:
        return EnrichData(
            statistics={},
            auctions={},
            jk_urls={},
            geo_urls={},
            can_update_edit_dates={},
        ), {}

    data = await asyncio.gather(
        _load_statistic(offer_ids),
        _load_auctions(offer_ids),
        _load_jk_urls(params.get_jk_ids()),
        _load_geo_urls(params.get_geo_url_params()),
        _load_can_update_edit_date(offer_ids),
    )

    params = {}
    degradation = {}
    for item in data:
        params[item.key] = item.value
        degradation[item.key] = item.degraded

    return EnrichData(**params), degradation


async def _load_statistic(offer_ids: List[int]) -> EnrichItem:
    # todo: https://jira.cian.tech/browse/CD-74478
    return EnrichItem(key='statistics', degraded=False, value={})


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


async def _load_can_update_edit_date(offer_ids: List[int]) -> EnrichItem:
    result = await can_update_edit_date_degradation_handler(offer_ids)

    return EnrichItem(key='can_update_edit_dates', degraded=result.degraded, value=result.value)
