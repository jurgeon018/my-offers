from typing import Set, cast

from cian_cache import cached

from my_offers.enums.regions import RealtyRegions
from my_offers.repositories.monolith_cian_realty import api_geo_get_regions
from my_offers.services.geo_subdomains.get_subdomain_by_location_id import get_subdomain_map


@cached(group='region_ids')
async def get_region_ids_cached() -> Set[int]:
    return await get_region_ids()


async def get_region_ids() -> Set[int]:
    region_ids: Set[int] = set()

    subdomains = await get_subdomain_map()
    region_ids.update(int(location_id) for location_id in subdomains)

    for region in await api_geo_get_regions():
        region_ids.add(region.id)

    region_ids.add(cast(int, RealtyRegions.moscow_and_area.value))
    region_ids.add(cast(int, RealtyRegions.st_petersburg_and_area.value))

    return region_ids
