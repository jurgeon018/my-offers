from typing import List, Optional, Tuple, Union

from pytils.numeral import choose_plural

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.agent_bonus import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import (
    Category,
    CoworkingOfferType,
    FlatType,
)


SQUARE_METER_SYMBOL = 'м²'

CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}

UNIT_TYPE = {
    AreaUnitType.sotka: 'сот.',
    AreaUnitType.hectare: 'га.',
}

FLAT_TITLE = {
    FlatType.studio: 'Квартира-студия',
    FlatType.open_plan: 'Кв. со своб. планировкой',
}

BASEMENT_FLOOR = {
    -1: 'полуподвал',
    -2: 'подвал',
}

OFFER_TITLES = {
    # commercial
    Category.office_sale: 'Офис',
    Category.office_rent: 'Офис',
    Category.shopping_area_rent: 'Торговая площадь',
    Category.shopping_area_sale: 'Торговая площадь',
    Category.warehouse_rent: 'Склад',
    Category.warehouse_sale: 'Склад',
    Category.free_appointment_object_rent: 'Помещение свободного назначения',
    Category.free_appointment_object_sale: 'Помещение свободного назначения',
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

WORKPLACES_TITLE_PLURAL = {
    CoworkingOfferType.fixed_workplace: (
        'закреплённое рабочее место',
        'закреплённых рабочих места',
        'закреплённых рабочих мест',
    ),
    CoworkingOfferType.flexible_workplace: (
        'незакреплённое рабочее место',
        'незакреплённых рабочих места',
        'незакреплённых рабочих мест',
    ),
}


def get_properties(object_model: ObjectModel) -> List[str]:
    min_area = object_model.min_area and int(object_model.min_area)
    total_area = object_model.total_area and int(object_model.total_area)
    floor_number = object_model.floor_number
    floors_count = object_model.building and object_model.building.floors_count
    category = object_model.category

    is_land = all([
        object_model.land and object_model.land.area and object_model.land.area_unit_type,
        category in [Category.land_sale, Category.commercial_land_rent, Category.commercial_land_sale]
    ])
    area = f'{total_area}\xa0{SQUARE_METER_SYMBOL}' if total_area else None

    title: Optional[str]
    is_coworking_office = object_model.coworking_offer_type and object_model.coworking_offer_type.is_office
    is_workplace: bool = (
        object_model.coworking_offer_type and
        (
            object_model.coworking_offer_type.is_flexible_workplace or
            object_model.coworking_offer_type.is_fixed_workplace
        )
    )
    if is_coworking_office:
        workplaces = f'на {object_model.workplace_count} чел.' if object_model.workplace_count else None
        title = ' '.join(filter(None, ('Отдельный офис', area, workplaces)))
        area = None  # чтобы еще раз не добавлять площадь
    elif is_workplace:
        title, floor_number = get_workplace_title(object_model=object_model, floor_number=floor_number)
    elif title := OFFER_TITLES.get(category):
        if object_model.can_parts and total_area and min_area:
            area = f'от\xa0{min_area}\xa0до\xa0{total_area}\xa0{SQUARE_METER_SYMBOL}'
        elif is_land:
            unit_type = UNIT_TYPE[object_model.land.area_unit_type]
            area = f'{object_model.land.area}\xa0{unit_type}'
    else:
        flat_type = object_model.flat_type
        rooms_count = object_model.rooms_count

        if rooms_count:
            title = f'{rooms_count}-комн.\xa0кв.' if 1 <= rooms_count <= 5 else 'Многокомн.\xa0кв.'

        if flat_type and (flat_type.is_studio or flat_type.is_open_plan):
            title = FLAT_TITLE[flat_type]

    floors = _get_floors(floor_number=floor_number, floors_count=floors_count)

    return list(filter(None, [title, area, floors]))


def _get_offer_title(*, object_model: ObjectModel, separator: str) -> str:
    return separator.join(get_properties(object_model))


def get_offer_title(object_model: ObjectModel) -> str:
    return _get_offer_title(object_model=object_model, separator=', ')


def get_mobile_offer_title(object_model: ObjectModel) -> str:
    return _get_offer_title(object_model=object_model, separator=' • ')


def _get_floors(floor_number: Optional[int], floors_count: Optional[int]) -> Optional[str]:
    if not floor_number:
        return None

    if floor_number in BASEMENT_FLOOR:
        return BASEMENT_FLOOR[floor_number]

    if floors_count:
        floors_name = f'{floor_number}/{floors_count}\xa0этаж'
    else:
        floors_name = f'{floor_number}\xa0этаж'

    return floors_name


def get_workplace_title(
        *,
        object_model: ObjectModel,
        floor_number: int = None,
) -> Tuple[str, Union[str, Optional[int]]]:
    plural_workplace_title = choose_plural(
        object_model.workplace_count,
        WORKPLACES_TITLE_PLURAL.get(object_model.coworking_offer_type),
    )
    workplace_title = (
       f'{object_model.workplace_count} {plural_workplace_title}'
    )
    if not floor_number and object_model.floor_from and object_model.floor_to:
        floor_range: str = f'{object_model.floor_from}-{object_model.floor_to}'
        return workplace_title, floor_range
    return workplace_title, floor_number
