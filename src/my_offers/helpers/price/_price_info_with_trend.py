from typing import Optional

from my_offers import entities, enums
from my_offers.helpers.price import get_price_info
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_price_info_with_trend(
        *,
        object_model: ObjectModel,
        old_price: Optional[float],
) -> entities.PriceInfoWithTrend:
    price_info = get_price_info(object_model)
    result = entities.PriceInfoWithTrend(
        exact=price_info.exact,
        range=price_info.range,
        trend=None,
    )
    price = object_model.bargain_terms.price
    if price and old_price and (abs(price - old_price) > 1):
        result.trend = enums.PriceTrend.inc if price > old_price else enums.PriceTrend.dec
    return result
