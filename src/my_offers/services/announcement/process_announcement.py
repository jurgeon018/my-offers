from typing import Dict, List

from my_offers import entities, enums
from my_offers.repositories import portresql
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
    offer = entities.Offer(
        offer_id=announcement['id'],
        master_user_id=announcement['userId'],  # TODO: определить мастераккаунт
        user_id=announcement['publishedUserId'],
        deal_type=deal_type,
        offer_type=offer_type,
        status_tab=_get_status_tab(announcement.get('flags', {}).get('isArchived', False), announcement['status']),
        search_text=_get_search_text(announcement),
        row_version=announcement.get('rowVersion', 0),
        raw_data=announcement,
        services=_get_services(announcement.get('publishTerms', {}).get('terms', [])),
        is_manual=announcement['source'] != 'upload',
        is_in_hidden_base=announcement.get('isInHiddenBase', False),
        has_photo=bool(announcement['photos']),
    )

    await portresql.save_offer(offer)


def _get_status_tab(is_archived: bool, offer_status: str) -> enums.OfferStatusTab:
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

    return ' '.join(result)


def _get_services(terms: Dict) -> List[enums.Services]:
    result = []
    for term in terms:
        for service in term['services']:
            result.append(enums.Services(service))

    return result
