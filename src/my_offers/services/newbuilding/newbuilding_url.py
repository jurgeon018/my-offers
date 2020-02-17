from typing import Optional

from cian_cache import cached

from my_offers.repositories.newbuilding_search import v1_get_newbuildings_by_ids
from my_offers.repositories.newbuilding_search.entities import GetNewBuildingsByIdsRequest


@cached(group='newbuilding_url')
async def get_newbuilding_url_cached(jk_id: int) -> Optional[str]:
    return await get_newbuilding_url(jk_id)


async def get_newbuilding_url(jk_id: int) -> Optional[str]:
    response = await v1_get_newbuildings_by_ids(GetNewBuildingsByIdsRequest(ids=[jk_id]))
    for item in response.items:
        if item.id == jk_id:
            return item.url

    return None
