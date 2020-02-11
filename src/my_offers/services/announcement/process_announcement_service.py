from datetime import datetime
from typing import Dict, List, Optional, Tuple

from my_offers import entities, enums
from my_offers.mappers.date_time import date_time_time_zone_mapper
from my_offers.repositories import postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category


CATEGORY_OFFER_TYPE_DEAL_TYPE = {
    Category.flat_sale: (enums.OfferType.flat, enums.DealType.sale),
    Category.room_sale: (enums.OfferType.flat, enums.DealType.sale),
    Category.new_building_flat_sale: (enums.OfferType.flat, enums.DealType.sale),
    Category.flat_share_sale: (enums.OfferType.flat, enums.DealType.sale),
    Category.house_sale: (enums.OfferType.suburban, enums.DealType.sale),
    Category.cottage_sale: (enums.OfferType.suburban, enums.DealType.sale),
    Category.townhouse_sale: (enums.OfferType.suburban, enums.DealType.sale),
    Category.house_share_sale: (enums.OfferType.suburban, enums.DealType.sale),
    Category.land_sale: (enums.OfferType.suburban, enums.DealType.sale),

    Category.flat_rent: (enums.OfferType.flat, enums.DealType.rent),
    Category.room_rent: (enums.OfferType.flat, enums.DealType.rent),
    Category.bed_rent: (enums.OfferType.flat, enums.DealType.rent),
    Category.house_rent: (enums.OfferType.suburban, enums.DealType.rent),
    Category.cottage_rent: (enums.OfferType.suburban, enums.DealType.rent),
    Category.townhouse_rent: (enums.OfferType.suburban, enums.DealType.rent),
    Category.house_share_rent: (enums.OfferType.suburban, enums.DealType.rent),

    Category.daily_flat_rent: (enums.OfferType.flat, enums.DealType.rent),
    Category.daily_room_rent: (enums.OfferType.flat, enums.DealType.rent),
    Category.daily_bed_rent: (enums.OfferType.flat, enums.DealType.rent),
    Category.daily_house_rent: (enums.OfferType.suburban, enums.DealType.rent),

    Category.office_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.warehouse_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.shopping_area_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.industry_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.building_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.free_appointment_object_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.business_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.commercial_land_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.garage_sale: (enums.OfferType.commercial, enums.DealType.sale),
    # region v1
    Category.public_catering_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.car_service_sale: (enums.OfferType.commercial, enums.DealType.sale),
    Category.domestic_services_sale: (enums.OfferType.commercial, enums.DealType.sale),
    # endregion

    Category.office_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.warehouse_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.shopping_area_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.industry_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.building_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.free_appointment_object_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.business_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.commercial_land_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.garage_rent: (enums.OfferType.commercial, enums.DealType.rent),
    # region v1
    Category.public_catering_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.car_service_rent: (enums.OfferType.commercial, enums.DealType.rent),
    Category.domestic_services_rent: (enums.OfferType.commercial, enums.DealType.rent),
    # endregion
}

STATUS_TO_TAB_MAP = {
    enums.OfferStatus.published: enums.OfferStatusTab.active,

    enums.OfferStatus.draft: enums.OfferStatusTab.not_active,
    enums.OfferStatus.deactivated: enums.OfferStatusTab.not_active,
    enums.OfferStatus.sold: enums.OfferStatusTab.not_active,

    enums.OfferStatus.refused: enums.OfferStatusTab.declined,
    enums.OfferStatus.moderate: enums.OfferStatusTab.declined,
    enums.OfferStatus.removed_by_moderator: enums.OfferStatusTab.declined,
    enums.OfferStatus.blocked: enums.OfferStatusTab.declined,

    enums.OfferStatus.deleted: enums.OfferStatusTab.deleted,
}


async def process_announcement(announcement: Dict) -> None:
    offer_type, deal_type = CATEGORY_OFFER_TYPE_DEAL_TYPE[Category(announcement['category'])]
    status_tab = _get_status_tab(
        is_archived=announcement.get('flags', {}).get('isArchived', False),
        offer_status=announcement['status'],
    )

    total_area = _get_total_area(
        total_area=announcement.get('totalArea'),
        land=announcement.get('land'),
    )
    price, price_per_meter = _get_prices(
        bargain_terms=announcement['bargainTerms'],
        total_area=total_area,
    )

    offer = entities.Offer(
        offer_id=announcement['id'],
        master_user_id=announcement['userId'],  # TODO: определить мастераккаунт
        user_id=announcement['publishedUserId'],
        deal_type=deal_type,
        offer_type=offer_type,
        status_tab=status_tab,
        search_text=_get_search_text(announcement),
        row_version=announcement['rowVersion'],
        raw_data=announcement,
        services=_get_services(announcement.get('publishTerms', {}).get('terms', [])),
        is_manual=announcement['source'] != 'upload',
        is_in_hidden_base=announcement.get('isInHiddenBase', False),
        has_photo=bool(announcement['photos']),
        is_test=_get_is_test(announcement),
        price=price,
        price_per_meter=price_per_meter,
        total_area=total_area,
        walking_time=_get_walking_time(announcement.get('geo')),
        street_name=_get_street_name(announcement.get('geo', {}).get('address')),
        sort_date=_get_sort_date(announcement=announcement, status_tab=status_tab),
    )

    await postgresql.save_offer(offer)


def _get_status_tab(*, is_archived: bool, offer_status: str) -> enums.OfferStatusTab:
    # Логика работы вкладок
    # -- вкладка активные
    # 'published',
    # -- вкладка неактивные
    # 'draft',
    # 'deactivated',
    # 'sold',
    # -- вкладка отклоненные
    # 'refused',
    # 'moderate',
    # 'removed_by_moderator',
    # 'blocked',
    # -- вкладка архивные
    # флаг из isArchived
    # -- Удаленные
    # 'deleted'
    if is_archived:
        return enums.OfferStatusTab.archived

    status = enums.OfferStatus(offer_status)

    return STATUS_TO_TAB_MAP[status]


def _get_search_text(announcement: Dict) -> str:
    result = [str(announcement['id'])]
    if announcement.get('title'):
        result.append(announcement['title'])

    result.append(announcement['description'])

    for phone in announcement['phones']:
        if phone.get('countryCode') and phone.get('number'):
            result.append(phone['countryCode'] + phone['number'])
        if source_phone := phone.get('sourcePhone'):
            result.append(source_phone.get('countryCode') + source_phone.get('number'))

    if address := announcement.get('geo', {}).get('userInput'):
        result.append(address)

    if undergrounds := announcement.get('geo', {}).get('undergrounds'):
        for underground in undergrounds:
            result.append(underground['name'])

    return ' '.join(result)


def _get_services(terms: Dict) -> List[enums.Services]:
    result = []
    for term in terms:
        for service in term['services']:
            result.append(enums.Services(service))

    return result


def _get_is_test(announcement: Dict) -> bool:
    return announcement.get('platform', {}).get('type') == 'qaAutotests'


def _get_prices(*, bargain_terms: Dict, total_area: Optional[float] = None) -> Tuple[Optional[float], Optional[float]]:
    price: Optional[float] = None
    price_per_meter: Optional[float] = None
    price_type = bargain_terms['priceType']

    if price_type == 'all':
        price = bargain_terms['price']
        if total_area and price:
            price_per_meter = round(price / total_area, 2)
    else:
        kf = _area_to_meters_kf(price_type)

        price_per_meter = round(bargain_terms['price'] / kf, 2)
        if total_area and price_per_meter:
            price = price_per_meter * total_area

    return price, price_per_meter


def _area_to_meters_kf(unit_type: str) -> int:
    if unit_type == 'sotka':
        kf = 100
    elif unit_type == 'hectare':
        kf = 10000
    else:
        kf = 1

    return kf


def _get_total_area(*, total_area: Optional[float], land: Optional[Dict]) -> Optional[float]:
    if total_area:
        return total_area

    if not land:
        return None

    result = None
    area = land.get('area')
    unit_type = land.get('areaUnitType')
    if area and unit_type:
        result = area * _area_to_meters_kf(unit_type)

    return result


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


def _get_street_name(address: Optional[List]) -> Optional[str]:
    street_name = None
    if not address:
        return street_name

    for item in address:
        if item.get('type') == 'street' and item.get('name'):
            street_name = item['name']
            break

    return street_name


def _get_sort_date(*, announcement: Dict, status_tab: enums.OfferStatusTab) -> Optional[datetime]:
    field = 'archivedDate' if status_tab.is_archived else 'editDate'
    if result := announcement.get(field):
        result = date_time_time_zone_mapper.map_from(result)

    return result
