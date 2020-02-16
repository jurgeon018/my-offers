from typing import List, Optional, Tuple

from simple_settings import settings

from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, PriceInfo, Underground
from my_offers.enums import DealType, OfferType
from my_offers.enums.offer_address import AddressType
from my_offers.helpers.numbers import get_pretty_number
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Geo, ObjectModel, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.announcement.process_announcement_service import CATEGORY_OFFER_TYPE_DEAL_TYPE


SQUARE_METER_SYMBOL = 'м²'

CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}

OFFER_TITLES = {
    # commercial
    Category.office_sale: 'Офис',
    Category.office_rent: 'Офис',
    Category.shopping_area_rent: 'Торговая площадь',
    Category.shopping_area_sale: 'Торговая площадь',
    Category.warehouse_rent: 'Склад',
    Category.warehouse_sale: 'Склад',
    Category.free_appointment_object_rent: 'Свободное назначение',
    Category.free_appointment_object_sale: 'Свободное назначение',
    Category.public_catering_rent: 'Общепит',
    Category.public_catering_sale: 'Общепит',
    Category.garage_rent: 'Гараж',
    Category.garage_sale: 'Гараж',
    Category.industry_rent: 'Производство',
    Category.industry_sale: 'Производство',
    Category.car_service_rent: 'Автосервис',
    Category.car_service_sale: 'Автосервис',
    Category.business_rent: 'Готовый бизнес',
    Category.business_sale: 'Готовый бизнес',
    Category.building_sale: 'Здание',
    Category.building_rent: 'Здание',
    Category.domestic_services_rent: 'Бытовые услуги',
    Category.domestic_services_sale: 'Бытовые услуги',
    Category.commercial_land_rent: 'Коммерческая земля',
    Category.commercial_land_sale: 'Коммерческая земля',

    # suburban
    Category.house_sale: 'Дом',
    Category.house_rent: 'Дом',
    Category.daily_house_rent: 'Дом',
    Category.house_share_rent: 'Часть дома',
    Category.house_share_sale: 'Часть дома',
    Category.cottage_rent: 'Коттедж',
    Category.cottage_sale: 'Коттедж',
    Category.townhouse_sale: 'Таунхаус',
    Category.townhouse_rent: 'Таунхаус',
    Category.land_sale: 'Земельный участок',

    # flat
    # для flat_sale, flat_rent генерируется название из кол-ва комнат
    Category.daily_room_rent: 'Комната',
    Category.room_rent: 'Комната',
    Category.room_sale: 'Комната',
    Category.bed_rent: 'Койко-место',
    Category.daily_bed_rent: 'Койко-место',
    Category.flat_share_sale: 'Доля в квартире',
}

FLAT_TITLE = {
    FlatType.studio: 'Квартира-студия',
    FlatType.open_plan: 'Квартира со свободной планир.',
}

BASEMENT_FLOOR = {
    -1: 'полуподвал',
    -2: 'подвал',
}

UNIT_TYPE = {
    AreaUnitType.sotka: 'сот.',
    AreaUnitType.hectare: 'га.',
}


def build_offer_view(object_model: ObjectModel) -> GetOffer:
    """ Собирает из шарповой модели компактное представление объявления для выдачи.
    """
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    url_to_offer = _get_offer_url(
        offer_id=object_model.id,
        category=object_model.category
    )
    title = _get_title(
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
        total_area=object_model.total_area
    )
    features = _get_features(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category
    )
    publish_features = _get_publish_features(
        publish_terms=object_model.publish_terms,
        category=object_model.category
    )

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=title,
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=geo,
        subagent=subagent,
        price_info=price_info,
        features=features,
        publish_features=publish_features,
        vas=_get_vas(publish_terms=object_model.publish_terms),
        is_from_package=_is_from_package(publish_terms=object_model.publish_terms),
        is_manual=is_manual,
        is_publication_time_ends=_is_publication_time_ends(object_model),
        statistics=Statistics()
    )


def _get_offer_url(*, offer_id: int, category: Category) -> Optional[str]:
    offer_type, deal_type = _get_deal_type(category)

    if offer_id and category:
        return f'{settings.CiAN_BASE_URL}/{deal_type.value}/{offer_type.value}/{offer_id}'

    return None


def _get_title(*, object_model: ObjectModel, category: Category) -> str:
    offer_type, _ = _get_deal_type(category)
    min_area = object_model.min_area and int(object_model.min_area)
    total_area = object_model.total_area and int(object_model.total_area)
    floor_number = object_model.floor_number
    floors_count = object_model.building and object_model.building.floors_count
    is_land = all([
        object_model.land and object_model.land.area and object_model.land.area_unit_type,
        category in [Category.land_sale, Category.commercial_land_rent, Category.commercial_land_sale]
    ])

    area = None

    if title := OFFER_TITLES.get(category):
        if object_model.can_parts and total_area and min_area:
            area = f'от {min_area} до {total_area} {SQUARE_METER_SYMBOL}'

        elif is_land:
            unit_type = UNIT_TYPE[object_model.land.area_unit_type]
            area = f'{object_model.land.area} {unit_type}'
        else:
            area = f'{total_area} {SQUARE_METER_SYMBOL}'

    else:
        flat_type = object_model.flat_type
        rooms_count = object_model.rooms_count
        area = f'{total_area} {SQUARE_METER_SYMBOL}' if total_area else None

        if rooms_count:
            title = f'{rooms_count}-комн. кв.' if 1 <= rooms_count <= 5 else f'Многокомн. кв.'

        if flat_type and (flat_type.is_studio or flat_type.is_open_plan):
            title = FLAT_TITLE[flat_type]

    floors = _get_floors(floor_number=floor_number, floors_count=floors_count)
    title = ', '.join(filter(None, [title, area, floors]))

    return title


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
    max_area: Optional[float],
    total_area: Optional[float]
) -> PriceInfo:
    offer_type, deal_type = _get_deal_type(category)

    is_rent = deal_type.is_rent
    is_daily_rent = category in [
        Category.daily_flat_rent,
        Category.daily_room_rent,
        Category.daily_bed_rent,
        Category.daily_house_rent,
    ]
    is_square_meter = bargain_terms.price_type and bargain_terms.price_type.is_square_meter
    can_calc_parts = all([is_square_meter, offer_type.is_commercial, can_parts])

    currency = CURRENCY.get(bargain_terms.currency)
    price = int(bargain_terms.price)
    price_exact = None
    price_range = None

    if currency:
        pretty_price = get_pretty_number(number=price)

        if is_daily_rent:
            price_exact = f'{pretty_price} {currency}/сут.'

        elif is_rent:
            # mypy не понимает вычисления в all([..., max_area, min_area])
            if can_calc_parts and max_area and min_area:
                months_count = 12
                min_price = get_pretty_number(number=int(price / months_count * min_area))
                max_price = get_pretty_number(number=int(price / months_count * max_area))
                price_range = [f'от {min_price}', f'до {max_price} {currency}/мес']
            else:
                price = int(price * total_area) if is_square_meter and total_area else price
                pretty_price = get_pretty_number(number=price)
                price_exact = f'{pretty_price} {currency}/мес.'

        else:
            price_exact = f'{pretty_price} {currency}'

    return PriceInfo(exact=price_exact, range=price_range)


def _get_publish_features(publish_terms: PublishTerms, category: Category) -> Optional[List[str]]:
    # TODO: https://jira.cian.tech/browse/CD-74186
    if not publish_terms:
        return None

    is_daily_rent = category in [
        Category.daily_flat_rent,
        Category.daily_room_rent,
        Category.daily_bed_rent,
        Category.daily_house_rent,
    ]

    features = []
    if publish_terms.autoprolong and not is_daily_rent:
        features.append('автопродление')

    return features


def _get_features(*, bargain_terms: BargainTerms, category: Category) -> List[str]:
    offer_type, deal_type = _get_deal_type(category)
    is_sale = deal_type.is_sale
    is_rent = deal_type.is_rent
    is_commercial = offer_type.is_commercial
    is_newobject = category.is_new_building_flat_sale

    currency = CURRENCY.get(bargain_terms.currency)
    is_square_meter = bargain_terms.price_type and bargain_terms.price_type.is_square_meter
    is_all = bargain_terms.price_type and bargain_terms.price_type.is_all
    sale_type = bargain_terms.sale_type
    lease_type = bargain_terms.lease_type

    features = []

    # TODO: https://jira.cian.tech/browse/CD-74195
    if is_sale:
        if bargain_terms.mortgage_allowed:
            features.append('Возможна ипотека')

        if sale_type and sale_type.is_free:
            features.append('Свободная продажа')

        if sale_type and sale_type.is_alternative:
            features.append('Альтернативная продажа')

        if (is_commercial or is_newobject) and is_square_meter and currency:
            pretty_price = get_pretty_number(number=int(bargain_terms.price))
            features.append(f'{pretty_price} {currency} {SQUARE_METER_SYMBOL}')

        if not offer_type.is_commercial and sale_type and sale_type.is_dupt:
            features.append('Переуступка')

    if is_rent:
        if bargain_terms.agent_fee:
            features.append(f'Агенту: {bargain_terms.agent_fee}%')

        if bargain_terms.client_fee:
            features.append(f'Клиенту: {bargain_terms.client_fee}%')

        if bargain_terms.deposit and currency:
            features.append(f'Залог: {bargain_terms.deposit} {currency}')

        if is_commercial:
            if is_all and currency:
                pretty_price = get_pretty_number(number=int(bargain_terms.price))
                features.append(f'{pretty_price} {currency} за {SQUARE_METER_SYMBOL}')

            if is_square_meter and currency:
                months = 12
                pretty_price = get_pretty_number(number=int(bargain_terms.price * months))
                features.append(f'{pretty_price} {currency} за {SQUARE_METER_SYMBOL} в год')

            if lease_type and lease_type.is_sublease:
                features.append('Субаренда')

            if lease_type and lease_type.is_direct:
                features.append('Прямая аренда')

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


def _get_floors(floor_number: Optional[int], floors_count: Optional[int]) -> Optional[str]:
    floors_name = None
    if floor_number:
        if floor_number in BASEMENT_FLOOR:
            floors_name = BASEMENT_FLOOR[floor_number]
        else:
            if floors_count:
                floors_name = f'{floor_number}/{floors_count} этаж'
            else:
                floors_name = f'{floor_number} этаж'

    return floors_name
