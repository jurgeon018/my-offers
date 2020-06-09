import pytest

from my_offers.services.valuation.helpers.pretty_price import get_pretty_market_price, get_pretty_price_diapason


@pytest.mark.parametrize(
    ('price', 'need_million_str', 'expected'),
    (
        (1_000, True, '1\xa0000'),
        (100_000, True, '100\xa0000'),
        (999_000, True, '999\xa0000'),
        (1_000_000, True, '1 млн'),
        (11_230_000, True, '11,23 млн'),
        (1_000_000, False, '1'),
        (11_230_000, False, '11,23'),

    )
)
def test_get_pretty_market_price(mocker, price, need_million_str, expected):
    # arrange & act
    result = get_pretty_market_price(
        price=price,
        need_million_str=need_million_str,
    )

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('price_min', 'price_max', 'expected'),
    (
        (1_000, 2_000, '1\xa0000—2\xa0000'),
        (100_000, 200_000, '100\xa0000—200\xa0000'),
        (900_000, 998_000, '900\xa0000—998\xa0000'),
        (900_000, 1_000_000, '0,9—1\xa0млн'),
        (100_990_000, 110_800_000, '100,99—110,8\xa0млн'),

    )
)
def test_get_pretty_price_diapason(mocker, price_min, price_max, expected):
    # arrange & act
    result = get_pretty_price_diapason(
        price_min=price_min,
        price_max=price_max,
    )

    # assert
    assert result == expected
