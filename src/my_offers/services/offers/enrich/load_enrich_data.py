import asyncio
from typing import Dict, List

from my_offers.entities.enrich import AddressUrlParams
from my_offers.services.announcement.announcement_api import can_update_edit_date
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls_degradation_handler
from my_offers.services.offers.enrich.enrich_data import AddressUrls, EnrichData, EnrichParams, GeoUrlKey
from my_offers.services.seo_urls.get_seo_urls import get_query_strings_for_address_degradation_handler


async def load_enrich_data(params: EnrichParams) -> EnrichData:
    offer_ids = params.get_offer_ids()
    if not offer_ids:
        return EnrichData(
            statistics={},
            auctions={},
            jk_urls={},
            geo_urls={},
            can_update_edit_dates={},
        )

    data = await asyncio.gather(
        _load_statistic(offer_ids),  # 0
        _load_auctions(offer_ids),   # 1
        _load_jk_urls(params.get_jk_ids()),  # 2
        _load_geo_urls(params.get_geo_url_params()),  # 3
        _load_can_update_edit_date(offer_ids),  # 4
    )

    return EnrichData(
        statistics=data[0],
        auctions=data[1],
        jk_urls=data[2],
        geo_urls=data[3],
        can_update_edit_dates=data[4],
    )


async def _load_statistic(offer_ids: List[int]) -> Dict:
    # todo: https://jira.cian.tech/browse/CD-74478
    return {}


async def _load_auctions(offer_ids: List[int]) -> Dict:
    # todo: https://jira.cian.tech/browse/CD-74479
    return {}


async def _load_jk_urls(jk_ids: List[int]) -> Dict[int, str]:
    if not jk_ids:
        return {}

    result = await get_newbuilding_urls_degradation_handler(jk_ids)

    return result.value


async def _load_geo_urls(params: List[AddressUrlParams]) -> Dict[GeoUrlKey, AddressUrls]:
    result: Dict[GeoUrlKey, AddressUrls] = {}
    for param in params:
        data = await get_query_strings_for_address_degradation_handler(
            address_elements=param.address_info,
            deal_type=param.deal_type,
            offer_type=param.offer_type,
        )

        if data.degraded:
            continue

        for i, address in enumerate(param.address_info):
            key = GeoUrlKey(param.deal_type, param.offer_type)
            if key not in result:
                result[key] = AddressUrls()
            result[key].add_url(address=address, url=data.value[i])

    return result


async def _load_can_update_edit_date(offer_ids: List[int]) -> Dict[int, bool]:
    return await can_update_edit_date(offer_ids)
