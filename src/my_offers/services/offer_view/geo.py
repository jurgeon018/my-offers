from typing import List, Optional

from my_offers import enums
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import Geo


async def prepare_geo(*, geo: Geo, deal_type: enums.DealType, offer_type: enums.OfferType) -> OfferGeo:
    geo = OfferGeo(
        address=_get_address(geo),
        newbuilding=_get_newbuilding(geo),
        underground=_get_underground(geo)
    )

    return geo


def _get_underground(geo: Geo) -> Optional[Underground]:
    if not geo or not geo.undergrounds or not geo.address:
        return None

    # получаем основное метро
    undergrounds = list(filter(lambda x: x.is_default, geo.undergrounds))
    # определяем местоположение
    address = list(filter(lambda x: x.type.is_location, geo.address))

    if undergrounds and address:
        return Underground(
            search_url='',
            region_id=address[0].id,
            line_color=undergrounds[0].line_color,
            name=undergrounds[0].name
        )

    return None


def _get_newbuilding(geo: Geo) -> Optional[Newbuilding]:
    if not geo or not geo.jk:
        return None

    return Newbuilding(search_url='', name=geo.jk.name)


def _get_address(geo: Geo) -> Optional[List[Address]]:
    if not geo or not geo.address:
        return None

    addresses = []

    # TODO: Урдлы переходов в поиск (https://jira.cian.tech/browse/CD-74034)
    for address in geo.address:
        if address.type and address.full_name:
            if address.type.is_location:
                addresses.append(Address(search_url='', name=address.full_name, type=AddressType.location))
            elif address.type.is_district:
                addresses.append(Address(search_url='', name=address.full_name, type=AddressType.district))
            elif address.type.is_street:
                addresses.append(Address(search_url='', name=address.full_name, type=AddressType.street))
            elif address.type.is_house:
                addresses.append(Address(search_url='', name=address.full_name, type=AddressType.house))

    return addresses
