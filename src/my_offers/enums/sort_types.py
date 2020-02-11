from cian_enum import NoFormat, StrEnum


class GetOffersSortType(StrEnum):
    by_price_min = 'by_price_min'
    """По цене: убывающая"""
    by_price_max = 'by_price_max'
    """По цене: возрастающая"""
    by_price_for_meter = 'by_price_for_meter'
    """По цене за метр"""
    by_area_min = 'by_area_min'
    """По площади: убывающая"""
    by_area_max = 'by_area_max'
    """По площади: возрастающая"""
    by_walk_time = 'by_walk_time'
    """По времени до метро"""
    by_street = 'by_street'
    """По улице"""
    by_offer_id = 'by_offer_id'
    """По ID объявления"""
