from typing import List, Dict, Any

from cian_cache import cached
from cian_core.context import new_operation_id, get_operation_id
from simple_settings import settings

from my_offers.repositories.geo_subdomain import v1_get_subdomains


@cached(group='geo_subdomain_map', key='all')
async def get_subdomain_map() -> Dict[str, Dict[str, Any]]:
    with new_operation_id(operation_id=get_operation_id()):
        subdomains = await v1_get_subdomains()

    geo_subdomain_map = {}
    for subdomain in subdomains.subdomains:
        for location in subdomain['locations']:
            geo_subdomain_map[str(location['location_id'])] = subdomain
    return geo_subdomain_map


def get_subdomain_data_by_location_ids(
        *,
        location_ids: List[int],
        geo_subdomain_map: Dict[str, Any],
) -> Dict[str, Any]:
    for location_id in location_ids:
        result = geo_subdomain_map.get(str(location_id))
        if result is not None:
            return result

    return geo_subdomain_map.get(str(settings.DEFAULT_LOCATION_ID))
