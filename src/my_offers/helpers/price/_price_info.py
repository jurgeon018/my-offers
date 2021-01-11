from typing import List, Optional, Tuple

from simple_settings import settings

from my_offers import entities, enums
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_locations
from my_offers.helpers.numbers import get_pretty_number
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, RentByParts, UtilitiesTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, ObjectModel


CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}


def get_price_info(object_model: ObjectModel) -> entities.PriceInfo:
    offer_type, deal_type = get_types(object_model.category)
    bargain_terms = object_model.bargain_terms

    # для коворкинга
    coworking_offer_type = object_model.coworking_offer_type
    workplace_count = object_model.workplace_count
    if coworking_offer_type and coworking_offer_type.is_office and workplace_count:
        return _get_price_for_workplace(bargain_terms=bargain_terms, workplace_count=workplace_count)

    return _get_price_info(
        locations=get_locations(object_model.geo),
        bargain_terms=bargain_terms,
        category=object_model.category,
        can_parts=bool(object_model.can_parts),
        min_area=object_model.min_area,
        max_area=object_model.max_area,
        total_area=object_model.total_area,
        offer_type=offer_type,
        deal_type=deal_type,
        area_parts=object_model.area_parts,
    )


def _get_price_info(
        *,
        locations: List[int],
        bargain_terms: BargainTerms,
        category: Category,
        can_parts: bool,
        min_area: Optional[float],
        max_area: Optional[float],
        total_area: Optional[float],
        offer_type: enums.OfferType,
        deal_type: enums.DealType,
        area_parts: Optional[List[RentByParts]] = None,
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
    can_calc_parts = all([is_square_meter, offer_type.is_commercial, can_parts, max_area, min_area or area_parts])

    price_exact = None
    price_range = None
    pretty_price = get_pretty_number(price)
    if is_daily_rent:
        price_exact = f'{pretty_price}\xa0{currency}/сут.'
    elif is_rent:
        price_exact, price_range = _calc_rent_price(
            locations=locations,
            price=price,
            currency=currency,
            bargain_terms=bargain_terms,
            can_calc_parts=can_calc_parts,
            is_square_meter=is_square_meter,
            total_area=total_area,
            min_area=min_area,
            max_area=max_area,
            area_parts=area_parts,
        )
    elif can_parts and min_area and max_area:
        min_price = get_pretty_number(price * min_area / max_area)
        max_price = get_pretty_number(price)
        price_range = [f'от\xa0{min_price}', f'до\xa0{max_price}\xa0{currency}']
    else:
        price_exact = f'{pretty_price}\xa0{currency}'

    return entities.PriceInfo(exact=price_exact, range=price_range)


def _calc_rent_price(
        *,
        locations: List[int],
        price: float,
        currency: str,
        bargain_terms: BargainTerms,
        is_square_meter: bool,
        can_calc_parts: bool,
        min_area: Optional[float],
        max_area: Optional[float],
        total_area: Optional[float],
        area_parts: Optional[List[RentByParts]] = None,
) -> Tuple[Optional[str], Optional[List[str]]]:
    price_exact = None
    price_range = None
    utilities_delta = _calc_utilities_delta(
        locations=locations,
        utilities_terms=bargain_terms.utilities_terms,
    )

    if bargain_terms.payment_period and bargain_terms.payment_period.is_monthly:
        price_per_month = price + utilities_delta
    else:
        price_per_month = price / 12 + utilities_delta

    if can_calc_parts:
        price_range = []
        min_price: Optional[float] = None
        if min_area:
            min_price = price_per_month * min_area
        elif area_parts:
            min_price = min((x.price * x.area for x in area_parts if x.price and x.area), default=None)

        if min_price:
            pretty_price = get_pretty_number(min_price)
            price_range.append(f'от\xa0{pretty_price}')

        if max_area:
            max_price = get_pretty_number(price_per_month * max_area)
            price_range.append(f'до\xa0{max_price}\xa0{currency}/мес')
    else:
        if is_square_meter and total_area:
            price_per_month *= total_area

        pretty_price = get_pretty_number(price_per_month)
        price_exact = f'{pretty_price}\xa0{currency}/мес.'

    return price_exact, price_range


def _calc_utilities_delta(*, locations: List[int], utilities_terms: Optional[UtilitiesTerms]) -> float:
    if not utilities_terms:
        return 0

    if not utilities_terms.price:
        return 0

    if utilities_terms.included_in_price:
        return 0

    result = 0
    if settings.USE_INCLUDE_UTILITIES_TERMS_REGIONS:
        if set(settings.INCLUDE_UTILITIES_TERMS_REGIONS).intersection(set(locations)):
            result = utilities_terms.price
    elif not set(settings.EXCLUDE_UTILITIES_TERMS_REGIONS).intersection(set(locations)):
        result = utilities_terms.price

    return result


def _get_price_for_workplace(*, bargain_terms: BargainTerms, workplace_count: int) -> entities.PriceInfo:
    price_for_workplace = bargain_terms.price_for_workplace
    if not price_for_workplace:
        price_for_workplace = bargain_terms.price / workplace_count

    pretty_price = get_pretty_number(price_for_workplace)
    currency = CURRENCY.get(bargain_terms.currency)
    return entities.PriceInfo(
        exact=f'{pretty_price}\xa0{currency}/мес. за рабочее место'
    )
