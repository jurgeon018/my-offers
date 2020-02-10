from typing import List, Optional

from cian_core.runtime_settings import runtime_settings

from my_offers.entities.get_offers import GetOffer
from my_offers.entities.offer_view_model import Address, Geo, Newbuilding, PriceInfo, Subagent, Underground
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_offer_view(raw_offer: ObjectModel) -> GetOffer:
    main_photo_url = raw_offer.photos[0].mini_url if raw_offer.photos else None
    url_to_offer = 'runtime_settings.CIAN_PUBLIC_URL'

    geo = Geo(
        address=_get_address(raw_offer),
        newbuilding=_get_newbuilding(raw_offer),
        underground=_get_underground(raw_offer)
    )
    subagent = Subagent(
        id=raw_offer.published_user_id,
        # TODO: https://jira.cian.tech/browse/CD-73807
        name=''
    )

    # TODO: all list
    vas = [s for s in raw_offer.publish_terms.terms[0].services]

    return GetOffer(
        id=raw_offer.id,
        created_at=raw_offer.creation_date,
        title=raw_offer.title,
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=geo,
        subagent=subagent,
        price_info=_get_price(raw_offer),
        features=_get_features(raw_offer),
        publish_features=_get_publish_features(raw_offer),
        vas=vas,
        is_from_package=_is_from_package(raw_offer),
        is_from_import=raw_offer.source.is_upload,
        is_publication_time_ends=_is_publication_time_ends(raw_offer),
    )


def _is_publication_time_ends(raw_offer: ObjectModel):
    # TODO: calc
    return False


def _is_from_package(raw_offer: ObjectModel) -> bool:
    # TODO: publish_terms только для опубликованных
    return any(
        t.tariff_identificator.tariff_grid_type.is_service_package
        for t in raw_offer.publish_terms.terms
    )


def _get_price(raw_offer: ObjectModel) -> PriceInfo:
    deal_type = _get_deal_type(raw_offer)
    is_rent = deal_type.is_rent
    price = int(raw_offer.bargain_terms.price)

    if is_rent:
        exact_price = f'{price} Р/мес.'
    else:
        exact_price = f'{price} Р'

    return PriceInfo(
        exact_price=exact_price
    )


def _get_publish_features(raw_offer: ObjectModel):
    features = []

    if raw_offer.publish_terms.autoprolong:
        features.append('автопродление')

    if raw_offer.publish_terms.terms:
        days = raw_offer.publish_terms.terms[0].days
        features.append(f'осталось {days} д.')  # TODO: hours

    return features


def _get_features(raw_offer: ObjectModel) -> List[str]:
    features = []

    deal_type = _get_deal_type(raw_offer)
    is_sale = deal_type.is_sale
    is_rent = deal_type.is_rent

    if is_sale:
        if raw_offer.bargain_terms.mortgage_allowed:
            features.append('Возможна ипотека')

        if raw_offer.bargain_terms.sale_type.is_free:
            features.append('Свободная продажа')

    elif is_rent:
        if raw_offer.bargain_terms.agent_fee:
            features.append(f'Агенту: {raw_offer.bargain_terms.agent_fee}%')

        if raw_offer.bargain_terms.client_fee:
            features.append(f'Клиенту: {raw_offer.bargain_terms.client_fee}%')

        if raw_offer.bargain_terms.deposit:
            features.append(f'Залог: {raw_offer.bargain_terms.deposit}%')

    else:
        return []

    return features


def _get_underground(raw_offer: ObjectModel) -> Optional[Underground]:
    # получаем основное метро
    undergrounds = list(filter(lambda x: x.is_default, raw_offer.geo.undergrounds))
    # определяем город
    address = list(filter(lambda x: x.type.is_location, raw_offer.geo.address))

    if undergrounds and address:
        return Underground(
            url='',
            region_id=address[0].id,
            line_color=undergrounds[0].line_color,
            name=undergrounds[0].name
        )

    return None


def _get_newbuilding(raw_offer: ObjectModel) -> Optional[Newbuilding]:
    if not raw_offer.geo.jk:
        return None

    return Newbuilding(
        url='',
        name=raw_offer.geo.jk.name
    )


def _get_address(raw_offer: ObjectModel) -> Address:
    addresses = raw_offer.geo.address

    town = None
    district = None
    street = None
    house = None

    for address in addresses:
        if address.type.is_location:
            town = address.full_name
        elif address.type.is_district:
            district = address.full_name
        elif address.type.is_street:
            street = address.full_name
        elif address.type.is_house:
            house = address.full_name

    address_name = ', '.join(filter(None, [town, district, street, house]))

    return Address(url='', name=address_name)


def _get_deal_type(raw_offer: ObjectModel):
    from my_offers.services.announcement.process_announcement import CATEGORY_OFFER_TYPE_DEAL_TYPE

    offer_type, deal_type = CATEGORY_OFFER_TYPE_DEAL_TYPE[raw_offer.category]

    return deal_type
