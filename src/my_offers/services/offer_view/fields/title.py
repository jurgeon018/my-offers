from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.offer_view.constants import (
    BASEMENT_FLOOR,
    FLAT_TITLE,
    OFFER_TITLES,
    SQUARE_METER_SYMBOL,
    UNIT_TYPE,
)


def get_title(*, object_model: ObjectModel, category: Category) -> str:
    min_area = object_model.min_area and int(object_model.min_area)
    total_area = object_model.total_area and int(object_model.total_area)
    floor_number = object_model.floor_number
    floors_count = object_model.building and object_model.building.floors_count
    is_land = all([
        object_model.land and object_model.land.area and object_model.land.area_unit_type,
        category in [Category.land_sale, Category.commercial_land_rent, Category.commercial_land_sale]
    ])

    if title := OFFER_TITLES.get(category):
        if object_model.can_parts and total_area and min_area:
            area: Optional[str] = f'от {min_area} до {total_area} {SQUARE_METER_SYMBOL}'
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
