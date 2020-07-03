from datetime import datetime
from typing import List, Optional

from my_offers import entities, enums
from my_offers.helpers.numbers import get_pretty_number
from my_offers.helpers.time import get_aware_date
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Flags, ObjectModel, Photo
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Source


CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}


def is_archived(flags: Optional[Flags]) -> bool:
    return bool(flags and flags.is_archived)


def is_manual(source: Optional[Source]) -> bool:
    return not bool(source and source.is_upload)


def get_sort_date(*, object_model: ObjectModel, status_tab: enums.OfferStatusTab) -> Optional[datetime]:
    if status_tab.is_archived:
        result = object_model.archived_date
    elif object_model.edit_date:
        result = object_model.edit_date
    else:
        result = object_model.creation_date

    return get_aware_date(result)


def get_main_photo_url(
        photos: Optional[List[Photo]],
        better_quality: bool = False
) -> Optional[str]:
    if not photos:
        return None
    return photos[0].thumbnail_url if better_quality else photos[0].mini_url


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
) -> entities.PriceInfo:
    currency = CURRENCY.get(bargain_terms.currency)
    if not currency:
        return entities.PriceInfo(exact=None, range=None)
    price = bargain_terms.price
    if not price:
        return entities.PriceInfo(exact=None, range=None)

    max_area = max_area if max_area else total_area
    is_rent = deal_type.is_rent
    is_daily_rent = category in [
        Category.daily_flat_rent,
        Category.daily_room_rent,
        Category.daily_bed_rent,
        Category.daily_house_rent,
    ]
    is_square_meter = bargain_terms.price_type and bargain_terms.price_type.is_square_meter
    can_calc_parts = all([is_square_meter, offer_type.is_commercial, can_parts, max_area, min_area])

    price_exact = None
    price_range = None
    pretty_price = get_pretty_number(price)
    if is_daily_rent:
        price_exact = f'{pretty_price}\xa0{currency}/сут.'
    elif is_rent:
        if bargain_terms.payment_period and bargain_terms.payment_period.is_monthly:
            price_per_month = price
        else:
            price_per_month = price / 12

        if can_calc_parts:
            min_price = get_pretty_number(price_per_month * min_area)
            max_price = get_pretty_number(price_per_month * max_area)
            price_range = [f'от\xa0{min_price}', f'до\xa0{max_price}\xa0{currency}/мес']
        else:
            if is_square_meter and total_area:
                price_per_month *= total_area

            pretty_price = get_pretty_number(price_per_month)
            price_exact = f'{pretty_price}\xa0{currency}/мес.'
    elif can_parts and min_area and max_area:
        min_price = get_pretty_number(price * min_area / max_area)
        max_price = get_pretty_number(price)
        price_range = [f'от\xa0{min_price}', f'до\xa0{max_price}\xa0{currency}']
    else:
        price_exact = f'{pretty_price}\xa0{currency}'

    return entities.PriceInfo(exact=price_exact, range=price_range)
