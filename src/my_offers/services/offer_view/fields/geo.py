from my_offers.services.offers.enrich.enrich_data import AddressUrls
from typing import List, Optional, Dict

from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, Geo, Jk, UndergroundInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type


ADDRESS_TYPES_MAP = {
    Type.location: AddressType.location,
    Type.district: AddressType.district,
    Type.street: AddressType.street,
    Type.house: AddressType.house,
}


def prepare_geo(*, geo: Optional[Geo], geo_urls: AddressUrls, jk_urls: Dict[int, str]) -> OfferGeo:
    if not geo:
        return OfferGeo()

    geo = OfferGeo(
        address=_get_address(address_info=geo.address, urls=geo_urls),
        newbuilding=_get_newbuilding(jk=geo.jk, urls=jk_urls),
        underground=_get_underground(undergrounds_info=geo.undergrounds, address_info=geo.address, urls=geo_urls),
    )

    return geo


def _get_underground(
        *,
        undergrounds_info: Optional[List[UndergroundInfo]],
        address_info: Optional[List[AddressInfo]],
        urls: AddressUrls,
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
        search_url=urls.get_url(AddressInfo(type=Type.underground, id=underground.id)),
        region_id=address[0].id,
        line_color=underground.line_color,
        name=underground.name,
    )


def _get_newbuilding(jk: Optional[Jk], urls: Dict[int, str]) -> Optional[Newbuilding]:
    if not jk:
        return None

    return Newbuilding(
        search_url=urls.get(jk.id),
        name=jk.name,
    )


def _get_address(
        *,
        address_info: Optional[List[AddressInfo]],
        urls: AddressUrls,
) -> Optional[List[Address]]:
    if not address_info:
        return None

    result = []
    for address in address_info:
        if address.type and address.full_name and address.type in ADDRESS_TYPES_MAP:
            result.append(
                Address(
                    search_url=urls.get_url(address),
                    name=address.full_name,
                    type=ADDRESS_TYPES_MAP[address.type]
                )
            )

    return result
