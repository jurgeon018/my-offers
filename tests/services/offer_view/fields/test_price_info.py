import pytest

from my_offers import enums
from my_offers.entities.offer_view_model import PriceInfo
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import (
    Currency,
    PaymentPeriod,
    PriceType,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.offer_view.fields.price_info import get_price_info


@pytest.mark.parametrize(
    (
        'bargain_terms',
        'category',
        'can_parts',
        'min_area',
        'max_area',
        'total_area',
        'offer_type',
        'deal_type',
        'expected',
    ),
    (
        (
            BargainTerms(price=10000.0, currency=Currency.rur, price_type=PriceType.all),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.sale,
            PriceInfo(exact=None, range=['от 1 000', 'до 10 000 ₽']),
        ),
        (
            BargainTerms(
                price=10000.0,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.annual
            ),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.rent,
            PriceInfo(exact=None, range=['от 8 333', 'до 83 333 ₽/мес']),
        ),
        (
            BargainTerms(
                price=10000.0,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.monthly
            ),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.rent,
            PriceInfo(exact=None, range=['от 100 000', 'до 1 000 000 ₽/мес']),
        ),
    )
)
def test_get_price_info(
        bargain_terms,
        category,
        can_parts,
        min_area,
        max_area,
        total_area,
        offer_type,
        deal_type,
        expected,
):
    # arrange & act
    result = get_price_info(
        bargain_terms=bargain_terms,
        category=category,
        can_parts=can_parts,
        min_area=min_area,
        max_area=max_area,
        total_area=total_area,
        offer_type=offer_type,
        deal_type=deal_type,
    )

    # assert
    assert result == expected
