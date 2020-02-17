from typing import Tuple

from my_offers import enums
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


def get_types(category: Category) -> Tuple[enums.OfferType, enums.DealType]:
    return CATEGORY_OFFER_TYPE_DEAL_TYPE[category]
