from typing import List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, Geo, Jk, UndergroundInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_url_cached
from my_offers.services.seo_urls import get_query_strings_for_address


ADDRESS_TYPES_MAP = {
    Type.location: AddressType.location,
    Type.district: AddressType.district,
    Type.street: AddressType.street,
    Type.house: AddressType.house,
}


async def prepare_geo(*, geo: Optional[Geo], deal_type: enums.DealType, offer_type: enums.OfferType) -> OfferGeo:
    if not geo:
        return OfferGeo()

    geo = OfferGeo(
        address=await _get_address(address_info=geo.address, deal_type=deal_type, offer_type=offer_type),
        newbuilding=await _get_newbuilding(geo.jk),
        underground=await _get_underground(
            undergrounds_info=geo.undergrounds,
            address_info=geo.address,
            deal_type=deal_type,
            offer_type=offer_type,
        ),
    )

    return geo


async def _get_underground(
        *,
        undergrounds_info: Optional[List[UndergroundInfo]],
        address_info: Optional[List[AddressInfo]],
        deal_type: enums.DealType,
        offer_type: enums.OfferType,
) -> Optional[Underground]:
    if not undergrounds_info or not address_info:
        return None

    # получаем основное метро
    undergrounds = list(filter(lambda x: x.is_default, undergrounds_info))
    if not undergrounds:
        return None
    # определяем местоположение
    address = list(filter(lambda x: x.type and x.type.is_location, address_info))
    if not address:
        return None

    underground = undergrounds[0]
    return Underground(
        search_url=(await get_query_strings_for_address(
            address_elements=[AddressInfo(id=underground.id, type=Type.underground)],
            deal_type=deal_type,
            offer_type=offer_type,
        ))[0],
        region_id=address[0].id,
        line_color=underground.line_color,
        name=underground.name,
    )


async def _get_newbuilding(jk: Optional[Jk]) -> Optional[Newbuilding]:
    if not jk:
        return None

    return Newbuilding(
        search_url=await get_newbuilding_url_cached(jk.id),
        name='ЖК "{}"'.format(jk.name),
    )


async def _get_address(
        *,
        address_info: Optional[List[AddressInfo]],
        deal_type: enums.DealType,
        offer_type: enums.OfferType,
) -> Optional[List[Address]]:
    if not address_info:
        return None

    urls = await get_query_strings_for_address(
        address_elements=address_info,
        deal_type=deal_type,
        offer_type=offer_type,
    )

    addresses = []
    i = 0
    for address in address_info:
        if address.type and address.full_name and address.type in ADDRESS_TYPES_MAP:
            addresses.append(Address(search_url=urls[i], name=address.full_name, type=ADDRESS_TYPES_MAP[address.type]))
            i += 1

    return addresses
