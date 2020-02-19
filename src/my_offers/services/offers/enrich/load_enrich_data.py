import asyncio

from typing import Dict, List

from my_offers.entities.enrich import AddressUrlParams
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls_cached
from my_offers.services.offers.enrich.enrich_data import EnrichParams, EnrichData, AddressUrls
from my_offers.services.seo_urls import get_query_strings_for_address


async def load_enrich_data(params: EnrichParams) -> EnrichData:
    offer_ids = params.get_offer_ids()
    data = await asyncio.gather(
        _load_statistic(offer_ids),  # 0
        _load_auctions(offer_ids),   # 1
        _load_jk_urls(params.get_jk_ids()),  # 2
        _load_geo_urls(params.get_geo_url_params()),  # 3
    )

    return EnrichData(
        statistics=data[0],
        auctions=data[1],
        jk_urls=data[2],
        geo_urls=data[3],
    )


async def _load_statistic(offer_ids: List[int]) -> Dict:
    # todo: https://jira.cian.tech/browse/CD-74478
    return {}


async def _load_auctions(offer_ids: List[int]) -> Dict:
    # todo: https://jira.cian.tech/browse/CD-74479
    return {}


async def _load_jk_urls(js_ids: List[int]) -> Dict[int, str]:
    if not js_ids:
        return {}

    return await get_newbuilding_urls_cached(js_ids)


async def _load_geo_urls(params: List[AddressUrlParams]) -> Dict[tuple, AddressUrls]:
    result: Dict[tuple, AddressUrls] = {}
    for param in params:
        urls = await get_query_strings_for_address(
            address_elements=param.address_info,
            deal_type=param.deal_type,
            offer_type=param.offer_type,
        )

        for i, address in enumerate(param.address_info):
            key = (param.deal_type, param.offer_type)
            if key not in result:
                result[key] = AddressUrls()
            result[key].add_url(address=address, url=urls[i])

    return result
