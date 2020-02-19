from typing import Dict, List

from cian_cache import cached
from cian_core.degradation import get_degradation_handler

from my_offers.repositories.newbuilding_search import v1_get_newbuildings_by_ids
from my_offers.repositories.newbuilding_search.entities import GetNewBuildingsByIdsRequest


@cached(group='newbuilding_urls')
async def get_newbuilding_urls_cached(jk_ids: List[int]) -> Dict[int, str]:
    return await get_newbuilding_urls(jk_ids)


async def get_newbuilding_urls(jks_id: List[int]) -> Dict[int, str]:
    response = await v1_get_newbuildings_by_ids(GetNewBuildingsByIdsRequest(ids=jks_id))
    result = {}
    for item in response.items:
        if item.id:
            result[item.id] = item.url

    return result

get_newbuilding_urls_degradation_handler = get_degradation_handler(
    func=get_newbuilding_urls,
    key='get_newbuilding_urls',
    default={},
)
