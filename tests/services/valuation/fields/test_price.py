import pytest
from cian_web.exceptions import BrokenRulesException

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


@pytest.mark.parametrize(
    ('price', 'currency'),
    (
        (None, Currency.rur),
        (0, Currency.rur),
    )
)
def test_get_price_raise_exeption(mocker, price, currency):
    # arrange & act

    with pytest.raises(BrokenRulesException) as exc_info:
        get_price_rur(price=price, currency=currency)

    # assert
    assert exc_info.value.errors[0].key == 'price'
    assert exc_info.value.errors[0].code == 'valuation_not_poossible'
    assert exc_info.value.errors[0].message == 'offer object_model has uncorrect price ' \
                                               'valuation can not be provided without price'
