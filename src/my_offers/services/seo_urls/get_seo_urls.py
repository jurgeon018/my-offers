from copy import deepcopy
from typing import List, Any, Dict, Set

from my_offers.entities.seo_urls import GeoQueryParamsDict
from my_offers.enums import DealType, GeoType
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_python import internal_api_serialize_query_params
from my_offers.repositories.monolith_python.entities import SerializeToQueryStringsRequest
from my_offers.services.get_region_ids import get_region_ids_cached
from my_offers.services.seo_urls.constants import FIELDS_FOR_EXCLUDE, ALL_GEO_KEYS, GEO_KEYS_MAP


def get_geo_type_for_address_element(address_element: AddressInfo) -> GeoType:
    return GeoType(address_element.get('geoType') or 'underground')


def get_address_element_key(address_element: AddressInfo) -> str:
    return f'{get_geo_type_for_address_element(address_element).value}-{address_element["id"]}'


def make_query_params(
        *,
        address_element: AddressInfo,
        region_ids: Set[int],
        skip_foot: bool,
) -> GeoQueryParamsDict:
    params = {}
    geo_type = get_geo_type_for_address_element(address_element)
    if geo_type.is_underground and not skip_foot:
        params.update({'foot_min': 25, 'only_foot': '2'})

    if geo_type.is_location and address_element.id in region_ids:
        params_key = 'region'
    else:
        params_key = 'locations'
    geo_key = GEO_KEYS_MAP[geo_type]
    params[params_key] = [{geo_key: address_element.id}]
    params['engine_version'] = 2
    return params


def get_query_params_for_address_element(
        *,
        address_element: AddressInfo,
        query_params: Dict[str, Any],
        region_ids: Set[int],
        deal_type: DealType,
) -> Dict[str, Any]:
    skip_foot = deal_type.is_sale
    geo_query_params = make_query_params(address_element=address_element, region_ids=region_ids, skip_foot=skip_foot)

    return {
        **query_params,
        **geo_query_params
    }


async def get_query_strings_for_address(
        *,
        address_elements: List[AddressInfo],
        query_params: Dict[str, Any],
        deal_type: DealType,
) -> Dict[str, str]:
    query_params = deepcopy(query_params)

    for field in FIELDS_FOR_EXCLUDE:
        query_params.pop(field, None)

    for geo_key in ALL_GEO_KEYS:
        query_params.pop(geo_key, None)

    region_ids = await get_region_ids_cached()

    address_query_params = [
        get_query_params_for_address_element(
            deal_type=deal_type,
            address_element=elem,
            query_params=query_params,
            region_ids=region_ids,
        ) for elem in address_elements
    ]

    query_strings = await internal_api_serialize_query_params(
        SerializeToQueryStringsRequest(query_params=address_query_params),
    )
    query_strings = query_strings.data.query_strings

    address_element_ids = [
        get_address_element_key(elem) for elem in address_elements
    ]
    return dict(zip(address_element_ids, query_strings))
