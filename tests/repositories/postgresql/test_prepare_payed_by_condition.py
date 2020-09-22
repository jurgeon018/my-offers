import pytest

from my_offers.enums import OfferPayedByFilterType
from my_offers.repositories.postgresql.offer_conditions import OFFER_TABLE, _prepare_payed_by_condition


@pytest.mark.parametrize(
    ('filter', 'expected'), 
    [
        (OfferPayedByFilterType.any, None)
    ]
)
def test_prepare_payed_by_condition(filter, expected):
    # act
    result = _prepare_payed_by_condition(filter)

    # assert
    assert result == expected
