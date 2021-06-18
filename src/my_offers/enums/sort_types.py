from cian_enum import StrEnum


class GetOffersSortType(StrEnum):
    by_default = 'by_default'
    """По-умолчанию"""
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
    declined_date = 'declined_date'
    """Дата отклонения модерацией"""

class MobOffersSortType(StrEnum):
    update_date = 'updateDate'
    """По дате обновления"""
    move_to_archive_date = 'moveToArchiveDate'
    """По дате добавления в архив"""
    price_asc = 'priceAsc'
    """По цене по возрастанию"""
    price_desc = 'priceDesc'
    """По цене по убыванию"""
    declined_date = 'declinedDate'
    """Дата отклонения модерацией"""
