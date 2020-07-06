from typing import Optional, Tuple

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms
from my_offers.services.announcement.fields.prices import get_prices

PRICE_DEVIATION = 0.2


def get_range_price(
        *,
        bargain_terms: BargainTerms,
        total_area: Optional[float] = None
) -> Tuple[Optional[float], Optional[float]]:
    price, _ = get_prices(
        bargain_terms=bargain_terms,
        total_area=total_area
    )
    if not price:
        return None, None
    return price * (1 - PRICE_DEVIATION), price * (1 + PRICE_DEVIATION)
