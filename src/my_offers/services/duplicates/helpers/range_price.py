from typing import Optional, Tuple

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms
from my_offers.services.announcement.fields.prices import get_prices


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
    return price * 0.8, price * 1.2
