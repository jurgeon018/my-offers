import pytest

from my_offers.enums import OfferPayedByFilterType
from my_offers.repositories.postgresql.offer_conditions import _prepare_payed_by_condition


@pytest.mark.parametrize(
    ('filter', 'expected_none'),
    [
        (OfferPayedByFilterType.any.value, True),
        (OfferPayedByFilterType.by_agent.value, False),
        (OfferPayedByFilterType.by_master.value, False)
    ]
)
def test_prepare_payed_by_condition(filter, expected_none):
    # act
    result = _prepare_payed_by_condition(filter)

    # assert
    assert (result is None) == expected_none
