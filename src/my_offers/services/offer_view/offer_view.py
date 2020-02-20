from typing import Optional

from simple_settings import settings

from my_offers import enums
from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType
from my_offers.services.announcement.category import get_types
from my_offers.services.offer_view.constants import SQUARE_METER_SYMBOL
from my_offers.services.offer_view.fields.features import get_features
from my_offers.services.offer_view.fields.geo import prepare_geo
from my_offers.services.offer_view.fields.is_from_package import is_from_package
from my_offers.services.offer_view.fields.price_info import get_price_info
from my_offers.services.offer_view.fields.publish_features import get_publish_features
from my_offers.services.offer_view.fields.vas import get_vas


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


async def build_offer_view(object_model: ObjectModel) -> GetOffer:
    """ Собирает из шарповой модели компактное представление объявления для выдачи."""
    offer_type, deal_type = get_types(object_model.category)
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    url_to_offer = _get_offer_url(
        offer_id=object_model.id,
        offer_type=offer_type,
        deal_type=deal_type
    )
    title = _get_title(
        object_model=object_model,
        category=object_model.category,
    )

    subagent = None  # TODO: https://jira.cian.tech/browse/CD-73807
    is_manual = bool(object_model.source and object_model.source.is_upload)
    price_info = get_price_info(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category,
        can_parts=bool(object_model.can_parts),
        min_area=object_model.min_area,
        max_area=object_model.max_area,
        total_area=object_model.total_area,
        offer_type=offer_type,
        deal_type=deal_type
    )
    features = get_features(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category,
        total_area=object_model.total_area,
        offer_type=offer_type,
        deal_type=deal_type
    )
    publish_terms = object_model.publish_terms
    terms = publish_terms.terms if publish_terms else None

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=title,
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=await prepare_geo(geo=object_model.geo, deal_type=deal_type, offer_type=offer_type),
        subagent=subagent,
        price_info=price_info,
        features=features,
        publish_features=get_publish_features(publish_terms),
        vas=get_vas(terms),
        is_from_package=is_from_package(terms),
        is_manual=is_manual,
        is_publication_time_ends=_is_publication_time_ends(object_model),
        statistics=Statistics()
    )


def _get_offer_url(
        *,
        offer_id: int,
        offer_type: enums.OfferType,
        deal_type: enums.DealType
) -> str:
    return f'{settings.CiAN_BASE_URL}/{deal_type.value}/{offer_type.value}/{offer_id}'


def _get_title(*, object_model: ObjectModel, category: Category) -> str:
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


def _is_publication_time_ends(raw_offer: ObjectModel) -> bool:
    # TODO: https://jira.cian.tech/browse/CD-74186
    return False


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
