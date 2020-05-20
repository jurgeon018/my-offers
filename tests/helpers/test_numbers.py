import pytest

from my_offers.helpers.numbers import get_pretty_number


@pytest.mark.parametrize('number, expected', [
    (1, '1'),
    (100, '100'),
    (1000, '1\xa0000'),
    (10000, '10\xa0000'),
    (100000, '100\xa0000'),
    (1000000, '1\xa0000\xa0000'),
    (1000.5, '1\xa0001'),
    (1000.2, '1\xa0001'),
])
def test_get_pretty_number(number, expected):
    # act
    result = get_pretty_number(number)

    # assert
    assert result == expected
