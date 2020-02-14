from typing import List, Optional, Tuple

from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, PriceInfo, Underground
from my_offers.enums import DealType, OfferType
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Geo, ObjectModel, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.announcement.process_announcement_service import CATEGORY_OFFER_TYPE_DEAL_TYPE


CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}


def build_offer_view(object_model: ObjectModel) -> GetOffer:
    """ Собирает из шарповой модели компактное представление объявления для выдачи.
    """
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    url_to_offer = _get_offer_url(
        offer_id=object_model.id,
        category=object_model.category
    )
    tittle = _get_title(
        object_model=object_model,
        category=object_model.category
    )
    geo = OfferGeo(
        address=_get_address(object_model.geo),
        newbuilding=_get_newbuilding(object_model.geo),
        underground=_get_underground(object_model.geo)
    )
    subagent = None  # TODO: https://jira.cian.tech/browse/CD-73807
    is_manual = bool(object_model.source and object_model.source.is_upload)
    price_info = _get_price_info(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category,
        can_parts=bool(object_model.can_parts),
        min_area=object_model.min_area,
        max_area=object_model.max_area,
    )
    features = _get_features(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category
    )

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=tittle,
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=geo,
        subagent=subagent,
        price_info=price_info,
        features=features,
        publish_features=_get_publish_features(publish_terms=object_model.publish_terms),
        vas=_get_vas(publish_terms=object_model.publish_terms),
        is_from_package=_is_from_package(publish_terms=object_model.publish_terms),
        is_manual=is_manual,
        is_publication_time_ends=_is_publication_time_ends(object_model),
        statistics=Statistics()
    )


def _get_offer_url(*, offer_id: int, category: Category) -> Optional[str]:
    offer_type, deal_type = _get_deal_type(category)

    if offer_id and category:
        return f'http://cian.ru/{deal_type.value}/{offer_type.value}/{offer_id}'

    return None


def _get_title(*, object_model: ObjectModel, category: Category) -> str:
    offer_type, _ = _get_deal_type(category)
    min_area = object_model.min_area and int(object_model.min_area)
    total_area = object_model.total_area and int(object_model.total_area)
    rooms_count = object_model.rooms_count
    floor_number = object_model.floor_number
    floors_count = object_model.building and object_model.building.floors_count
    land = object_model.land
    can_parts = object_model.can_parts

    is_commercial = offer_type.is_commercial
    is_garage = category in [Category.garage_rent, Category.garage_sale]
    is_room = category in [Category.room_rent, Category.room_sale, Category.daily_room_rent]

    name = None

    if is_commercial and can_parts and total_area and min_area:
        name = f'Свободное назначение, от {min_area} до {total_area} м²'

    elif land and land.area:
        unit_type = 'сот.' if land.area_unit_type.is_sotka else 'га.'
        name = f'Участок {land.area} {unit_type}'

    elif is_garage:
        name = f'Машиноместо, {total_area} м²'

    else:

        area = None
        floors = None

        if rooms_count:
            flat_type = 'апарт.' if object_model.is_apartments else 'кв.'
            name = f'{rooms_count}-комн. {flat_type}' if 1 <= rooms_count < 5 else f'многокомн. {flat_type}'

        if total_area:
            area = f'{total_area} м²'

        if floor_number and floors_count:
            floors = f'{floor_number}/{floors_count} этаж'

        if is_room:
            name = f'Комната'

        name = ', '.join(filter(None, [name, area, floors]))

    return name


def _is_publication_time_ends(raw_offer: ObjectModel) -> bool:
    # TODO: https://jira.cian.tech/browse/CD-74186
    return False


def _is_from_package(publish_terms: PublishTerms) -> bool:
    if not publish_terms or not publish_terms.terms:
        return False

    # publish_terms только для опубликованных
    return any(
        term.tariff_identificator.tariff_grid_type.is_service_package
        for term in publish_terms.terms
        if term.tariff_identificator and term.tariff_identificator.tariff_grid_type
    )


def _get_vas(publish_terms: PublishTerms) -> Optional[List[Services]]:
    if not publish_terms or not publish_terms.terms:
        return None

    services: List[Services] = []
    for t in publish_terms.terms:
        if t.services:
            services.extend(t.services)

    return services


def _get_price_info(
        *,
        bargain_terms: BargainTerms,
        category: Category,
        can_parts: bool,
        min_area: Optional[float],
        max_area: Optional[float]
) -> PriceInfo:
    offer_type, deal_type = _get_deal_type(category)

    is_rent = deal_type.is_rent
    is_daily_rent = category in [
        Category.daily_flat_rent,
        Category.daily_room_rent,
        Category.daily_bed_rent,
        Category.daily_house_rent
    ]
    can_calc_parts = all([
        bargain_terms.price_type and bargain_terms.price_type.is_square_meter,
        offer_type.is_commercial,
        can_parts
    ])

    currency = CURRENCY.get(bargain_terms.currency)
    price = int(bargain_terms.price)
    price_exact = None
    price_range = None

    if currency:
        if is_daily_rent:
            price_exact = f'{price} {currency}/сут.'

        elif is_rent:
            # mypy не понимает вычисления в all([..., max_area, min_area])
            if can_calc_parts and max_area and min_area:
                months_count = 12
                min_price = int(price / months_count * min_area)
                max_price = int(price / months_count * max_area)
                price_range = [f'от {min_price}', f'до {max_price} {currency}/мес']
            else:
                price_exact = f'{price} {currency}/мес.'

        else:
            price_exact = f'{price} {currency}'

    return PriceInfo(exact=price_exact, range=price_range)


def _get_publish_features(publish_terms: PublishTerms) -> Optional[List[str]]:
    # TODO: https://jira.cian.tech/browse/CD-74186
    if not publish_terms:
        return None

    features = []

    if publish_terms.autoprolong:
        features.append('автопродление')

    return features


def _get_features(*, bargain_terms: BargainTerms, category: Category) -> List[str]:
    offer_type, deal_type = _get_deal_type(category)
    is_sale = deal_type.is_sale
    is_rent = deal_type.is_rent
    is_commercial = offer_type.is_commercial
    is_newobject = Category.is_new_building_flat_sale

    price = int(bargain_terms.price)
    currency = CURRENCY.get(bargain_terms.currency)
    is_square_meter = bargain_terms.price_type and bargain_terms.price_type.is_square_meter
    sale_type = bargain_terms.sale_type
    lease_type = bargain_terms.lease_type

    features = []

    # TODO: https://jira.cian.tech/browse/CD-74195
    if is_sale:
        if bargain_terms.mortgage_allowed:
            features.append('Возможна ипотека')

        if sale_type and sale_type.is_free:
            features.append('Свободная продажа')

        if is_commercial or is_newobject and is_square_meter and currency:
            features.append(f'{price} {currency} м²')

        if not offer_type.is_commercial and sale_type and sale_type.is_dupt:
            features.append('Переуступка')

    if is_rent:
        if bargain_terms.agent_fee:
            features.append(f'Агенту: {bargain_terms.agent_fee}%')

        if bargain_terms.client_fee:
            features.append(f'Клиенту: {bargain_terms.client_fee}%')

        if bargain_terms.deposit:
            features.append(f'Залог: {bargain_terms.deposit} {currency}')

        if is_commercial:
            if is_square_meter and currency:
                features.append(f'{price} {currency} за м² в год')

            if lease_type and lease_type.is_sublease:
                features.append('Субаренда')

            if lease_type and lease_type.is_direct:
                features.append('Прямая')

    return features


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
            line_color=f'#{undergrounds[0].line_color}',
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

    # TODO: Урлы переходов в поиск (https://jira.cian.tech/browse/CD-74034)
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


def _get_deal_type(category: Category) -> Tuple[OfferType, DealType]:
    offer_type, deal_type = CATEGORY_OFFER_TYPE_DEAL_TYPE[category]
    return offer_type, deal_type
