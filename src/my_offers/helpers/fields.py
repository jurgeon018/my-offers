from datetime import datetime
from typing import List, Optional

from my_offers import entities, enums
from my_offers.enums import OfferPayedByType
from my_offers.helpers.numbers import get_pretty_number
from my_offers.helpers.time import get_aware_date
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Flags, ObjectModel, Photo
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import (
    Category,
    CoworkingOfferType,
    Source,
    Status,
)
from my_offers.repositories.postgresql.billing import get_offer_publisher_user_id


CURRENCY = {
    Currency.rur: '₽',
    Currency.usd: '$',
    Currency.eur: '€',
}


def is_test(object_model: ObjectModel) -> bool:
    return (
        object_model.platform
        and object_model.platform.type
        and object_model.platform.type.is_qa_autotests
    )


def is_archived(flags: Optional[Flags]) -> bool:
    return bool(flags and flags.is_archived)


def is_manual(source: Optional[Source]) -> bool:
    return not bool(source and source.is_upload)


def is_draft(status: Optional[Status]) -> bool:
    return bool(status and status.is_draft)


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

    for photo in photos:
        if photo.is_default:
            break
    else:
        photo = photos[0]

    if better_quality and photo.thumbnail_url:
        return photo.thumbnail_url

    return photo.mini_url


def get_price_info(
        *,
        bargain_terms: BargainTerms,
        category: Category,
        can_parts: bool,
        min_area: Optional[float],
        max_area: Optional[float],
        total_area: Optional[float],
        offer_type: enums.OfferType,
        deal_type: enums.DealType,
        coworking_offer_type: Optional[CoworkingOfferType],
        workplace_count: Optional[int],
) -> entities.PriceInfo:
    if coworking_offer_type and coworking_offer_type.is_office and workplace_count:
        return _get_price_for_workplace(bargain_terms=bargain_terms, workplace_count=workplace_count)

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


def _get_price_for_workplace(*, bargain_terms: BargainTerms, workplace_count: int) -> entities.PriceInfo:
    price_for_workplace = bargain_terms.price_for_workplace
    if not price_for_workplace:
        price_for_workplace = bargain_terms.price / workplace_count

    pretty_price = get_pretty_number(price_for_workplace)
    currency = CURRENCY.get(bargain_terms.currency)
    return entities.PriceInfo(
        exact=f'{pretty_price}\xa0{currency}/мес. за рабочее место'
    )


def get_offer_payed_by(
        master_user_id: Optional[int],
        user_id: Optional[int],
        payed_by: Optional[int]
) -> Optional[enums.OfferPayedBy]:
    if not payed_by:
        return None
    if master_user_id == payed_by:
        return enums.OfferPayedBy.by_master
    if user_id == payed_by:
        return enums.OfferPayedBy.by_agent
    
    return None


async def get_payed_by(master_user_id: Optional[int], published_user_id: int, offer_id: int) -> Optional[OfferPayedByType]:
    publisher_user_id: int = await get_offer_publisher_user_id(offer_id)
    
    if not master_user_id or not publisher_user_id:
        return None
    elif publisher_user_id == published_user_id:
        return OfferPayedByType.by_agent
    elif publisher_user_id == master_user_id:
        return OfferPayedByType.by_master

    return None
