from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.newbuilding_search import v1_get_newbuildings_by_ids
from my_offers.repositories.newbuilding_search.entities import GetNewBuildingsByIdsRequest


async def get_newbuilding_urls(jk_ids: List[int]) -> Dict[int, str]:
    response = await v1_get_newbuildings_by_ids(GetNewBuildingsByIdsRequest(ids=jk_ids))
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
