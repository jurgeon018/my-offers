import pytest
from cian_test_utils import v

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import (
    Currency,
    PaymentPeriod,
    PriceType,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, CoworkingOfferType
from my_offers.services.offer_view.fields.features import get_features


@pytest.mark.parametrize(
    ('bargain_terms', 'category', 'total_area', 'offer_type', 'deal_type', 'expected'),
    (
        (
            BargainTerms(
                price=10000.0,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.annual
            ),
            Category.office_sale,
            10,
            enums.OfferType.commercial,
            enums.DealType.rent,
            ['10\xa0000 ₽ за м² в год'],
        ),
        (
            BargainTerms(
                price=10000.0,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.monthly,
            ),
            Category.office_sale,
            10,
            enums.OfferType.commercial,
            enums.DealType.rent,
            ['120\xa0000 ₽ за м² в год'],
        ),
        (
            BargainTerms(
                price=None,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.monthly,
            ),
            Category.office_sale,
            10,
            enums.OfferType.commercial,
            enums.DealType.rent,
            [],
        ),
        (
            BargainTerms(
                price=120,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.monthly,
            ),
            Category.office_sale,
            10,
            enums.OfferType.commercial,
            enums.DealType.sale,
            ['120 ₽ м²'],
        ),
        (
            BargainTerms(
                price=120,
                currency=Currency.rur,
                price_type=PriceType.all,
                payment_period=PaymentPeriod.monthly,
            ),
            Category.office_sale,
            10,
            enums.OfferType.commercial,
            enums.DealType.sale,
            ['12 ₽ за м²'],
        ),
    ),
)
def test_get_features(bargain_terms, category, total_area, offer_type, deal_type, expected):
    # arrange & act
    result = get_features(
        bargain_terms=bargain_terms,
        category=category,
        total_area=total_area,
        offer_type=offer_type,
        deal_type=deal_type,
        coworking_offer_type=None,
    )

    # assert
    assert result == expected


def test_get_features__coworking_office():
    # arrange
    bargain_terms = v(BargainTerms(price=10000.0, currency=Currency.rur))

    # act
    result = get_features(
        bargain_terms=bargain_terms,
        category=Category.office_rent,
        total_area=100,
        offer_type=enums.OfferType.commercial,
        deal_type=enums.DealType.rent,
        coworking_offer_type=CoworkingOfferType.office,
    )

    # assert
    assert result == ['10\xa0000\xa0₽/мес. за весь офис']
