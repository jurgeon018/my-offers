import pytest

from my_offers.helpers.numbers import get_pretty_number


@pytest.mark.parametrize('number, expected', [
    (1, '1'),
    (100, '100'),
    (1000, '1 000'),
    (10000, '10 000'),
    (100000, '100 000'),
    (1000000, '1 000 000'),
    (1000.5, '1 000'),
])
def test_get_pretty_number(number, expected):
    # act
    result = get_pretty_number(number=number)

    # assert
    assert result == expected
