from typing import Optional

from my_offers import enums
from my_offers.entities.offer_view_model import PriceInfo
from my_offers.helpers.numbers import get_pretty_number
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.offer_view.constants import CURRENCY


def get_price_info(
        *,
        bargain_terms: BargainTerms,
        category: Category,
        can_parts: bool,
        min_area: Optional[float],
        max_area: Optional[float],
        total_area: Optional[float],
        offer_type: enums.OfferType,
        deal_type: enums.DealType
) -> PriceInfo:
    max_area = max_area if max_area else total_area
    is_rent = deal_type.is_rent
    is_daily_rent = category in [
        Category.daily_flat_rent,
        Category.daily_room_rent,
        Category.daily_bed_rent,
        Category.daily_house_rent,
    ]
    is_square_meter = bargain_terms.price_type and bargain_terms.price_type.is_square_meter
    can_calc_parts = all([is_square_meter, offer_type.is_commercial, can_parts])

    currency = CURRENCY.get(bargain_terms.currency)

    price_exact = None
    price_range = None

    if not currency:
        return PriceInfo(exact=price_exact, range=price_range)

    price = int(bargain_terms.price)
    pretty_price = get_pretty_number(number=price)

    if is_daily_rent:
        price_exact = f'{pretty_price} {currency}/сут.'
    elif is_rent:
        # mypy не понимает вычисления в all([..., max_area, min_area])
        if can_calc_parts and max_area and min_area:
            if bargain_terms.payment_period and bargain_terms.payment_period.is_monthly:
                months_count = 1
            else:
                months_count = 12

            min_price = get_pretty_number(int(price / months_count * min_area))
            max_price = get_pretty_number(int(price / months_count * max_area))
            price_range = [f'от {min_price}', f'до {max_price} {currency}/мес']
        else:
            price = int(price * total_area) if is_square_meter and total_area else price
            pretty_price = get_pretty_number(price)
            price_exact = f'{pretty_price} {currency}/мес.'
    else:
        if can_parts and max_area and min_area:
            min_price = get_pretty_number(int(price * min_area / max_area))
            max_price = get_pretty_number(price)
            price_range = [f'от {min_price}', f'до {max_price} {currency}']
        else:
            price_exact = f'{pretty_price} {currency}'

    return PriceInfo(exact=price_exact, range=price_range)
