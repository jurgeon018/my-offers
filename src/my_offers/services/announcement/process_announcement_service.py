from typing import Dict, List, Optional

from my_offers import entities
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories import postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import ObjectModel
from my_offers.services.announcement.fields.category import get_types
from my_offers.services.announcement.fields.is_test import get_is_test
from my_offers.services.announcement.fields.prices import get_prices
from my_offers.services.announcement.fields.search_text import get_search_text
from my_offers.services.announcement.fields.sort_date import get_sort_date
from my_offers.services.announcement.fields.status_tab import get_status_tab
from my_offers.services.announcement.fields.street_name import get_street_name
from my_offers.services.announcement.fields.total_area import get_total_area
from my_offers.services.get_master_user_id import get_master_user_id


async def process_announcement(object_model: ObjectModel) -> None:
    offer_type, deal_type = get_types(object_model.category)
    status_tab = get_status_tab(
        is_archived=object_model.flags.is_archived if object_model.flags else False,
        offer_status=object_model.status,
    )

    total_area = get_total_area(total_area=object_model.total_area, land=object_model.land)
    price, price_per_meter = get_prices(bargain_terms=object_model.bargain_terms, total_area=total_area)
    geo = object_model.geo

    offer = entities.Offer(
        offer_id=object_model.id,
        master_user_id=await get_master_user_id(object_model.user_id),
        user_id=object_model.published_user_id,
        deal_type=deal_type,
        offer_type=offer_type,
        status_tab=status_tab,
        search_text=get_search_text(object_model),
        row_version=object_model.row_version,
        raw_data=object_model_mapper.map_to(object_model),
        services=object_model.publish_terms.terms.services if object_model.publish_terms else [],
        is_manual=not(object_model.source and object_model.source.is_upload),
        is_in_hidden_base=bool(object_model.is_in_hidden_base),
        has_photo=bool(object_model.photos),
        is_test=get_is_test(object_model),
        price=price,
        price_per_meter=price_per_meter,
        total_area=total_area,
        walking_time=_get_walking_time(geo),
        street_name=get_street_name(geo.address) if geo else None,
        sort_date=get_sort_date(object_model=object_model, status_tab=status_tab),
    )

    await postgresql.save_offer(offer)


def _get_walking_time(geo: Optional[Dict]) -> Optional[float]:
    walking_time = None

    if not geo:
        return walking_time

    walking_time = _get_walking_time_from_calculated_undergrounds(geo.get('calculatedUndergrounds'))
    if not walking_time:
        walking_time = _get_walking_time_from_undergrounds(geo.get('undergrounds'))

    return walking_time


def _get_walking_time_from_calculated_undergrounds(calculated_undergrounds: Optional[List]) -> Optional[float]:
    walking_time = None
    if not calculated_undergrounds:
        return walking_time

    for underground in calculated_undergrounds:
        if underground['transportType'] != 'walk':
            continue
        if not walking_time or underground['time'] < walking_time:
            walking_time = underground['time']

    return walking_time


def _get_walking_time_from_undergrounds(undergrounds: Optional[List]) -> Optional[float]:
    walking_time = None
    if not undergrounds:
        return walking_time

    min_transport_time = None

    for underground in undergrounds:
        time = underground.get('time')
        if not time:
            continue

        if underground['transportType'] == 'walk':
            if not walking_time or time < walking_time:
                walking_time = time
        elif underground['transportType'] == 'transport':
            if not min_transport_time or time < min_transport_time:
                min_transport_time = time

    if not walking_time and min_transport_time:
        # здесь умножаем на 10, потому что если человек идет
        # со срденей скоростью 4 км/ч, то автомобиль со скоростью 40 км/ч(в шарпе такие константы)
        # что в 10 раз больше
        # 2015 год python-monolith
        walking_time = min_transport_time * 10

    return walking_time
