import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, UtilitiesTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import (
    Currency,
    LeaseTermType,
    LeaseType,
    PaymentPeriod,
    PriceType,
    VatType,
)
from my_offers.services.announcement.fields.prices import get_prices


@pytest.mark.parametrize(
    ('bargain_terms', 'total_area', 'expected'),
    (
        (
            BargainTerms(
                price=11111.0,
                vat_type=VatType.usn,
                agent_fee=0,
                currency=Currency.rur,
                client_fee=0,
                lease_type=LeaseType.direct,
                price_type=PriceType.sotka,
                vat_included=True,
                prepay_months=3,
                lease_term_type=LeaseTermType.long_term,
                payment_period=PaymentPeriod.monthly,
                included_options=[],
            ),
            None,
            (None, 111.11),
        ),
        (
            BargainTerms(
                price=11111.0,
                vat_type=VatType.usn,
                agent_fee=0,
                currency=Currency.rur,
                client_fee=0,
                lease_type=LeaseType.direct,
                price_type=PriceType.all,
                vat_included=True,
                prepay_months=3,
                lease_term_type=LeaseTermType.long_term,
                payment_period=PaymentPeriod.monthly,
                included_options=[],
            ),
            None,
            (11111.0, None),
        ),
        (
            BargainTerms(
                price=11111.0,
                vat_type=VatType.usn,
                agent_fee=0,
                currency=Currency.rur,
                client_fee=0,
                lease_type=LeaseType.direct,
                price_type=PriceType.sotka,
                vat_included=True,
                prepay_months=3,
                lease_term_type=LeaseTermType.long_term,
                payment_period=PaymentPeriod.monthly,
                included_options=[],
            ),
            7,
            (777.77, 111.11),
        ),
        (
            BargainTerms(
                price=9070000.0,
                currency=Currency.rur,
                price_type=PriceType.all,
                included_options=[]
            ),
            90.7,
            (9070000.0, 100000.0),
        ),
        (
            BargainTerms(
                price=50000.0,
                vat_type=VatType.usn,
                agent_fee=5,
                currency=Currency.rur,
                client_fee=0,
                lease_type=LeaseType.direct,
                price_type=PriceType.hectare,
                vat_included=True,
                min_lease_term=6,
                prepay_months=1,
                lease_term_type=LeaseTermType.long_term,
                payment_period=PaymentPeriod.monthly,
                has_grace_period=True,
                included_options=[],
                security_deposit=20000,
            ),
            345,
            (1725.0, 5.0),
        ),
        (
            BargainTerms(
                price=360000.0,
                deposit=200000,
                vat_type=VatType.included,
                agent_fee=70,
                currency=Currency.rur,
                vat_price=60000.0,
                client_fee=70,
                price_type=PriceType.square_meter,
                vat_included=True,
                prepay_months=2,
                lease_term_type=LeaseTermType.long_term,
                payment_period=PaymentPeriod.monthly,
                bargain_allowed=False,
                utilities_terms=UtilitiesTerms(
                    price=0.0,
                    included_in_price=True,
                ),
                included_options=[]
            ),
            20,
            (7200000.0, 360000.0),
        ),
        (
            BargainTerms(price=77),
            90.7,
            (None, None),
        ),
    ),
)
def test__get_prices(bargain_terms, total_area, expected):
    # arrange & act
    result = get_prices(bargain_terms=bargain_terms, total_area=total_area)

    # assert
    assert result == expected
