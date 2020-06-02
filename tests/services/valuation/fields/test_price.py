import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.services.valuation.fields.price import get_price_rur


@pytest.mark.parametrize(
    ('price', 'currency', 'expected'),
    (
        (1_000_000, Currency.usd, 70_000_000),
        (1_000_000, Currency.eur, 80_000_000),
        (1_000_000, Currency.rur, 1_000_000),

    )
)
def test_get_price(mocker, price, currency, expected):
    # arrange & act
    result = get_price_rur(price=price, currency=currency)

    # assert
    assert result == expected
