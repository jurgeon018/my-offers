import pytest

from my_offers.enums import OfferPayedByFilterType
from my_offers.repositories.postgresql.offer_conditions import prepare_conditions


def test_prepare_payed_by_condition_call(mocker):
    _prepare_payed_by_condition = mocker.patch('my_offers.repositories.postgresql.offer_conditions'
                                               '._prepare_payed_by_condition')

    prepare_conditions(
        {'payed_by': 'any'}
    )

    assert _prepare_payed_by_condition.called


@pytest.mark.parametrize('payed_by, non_empty', [
    (OfferPayedByFilterType.by_agent.value, True),
    (OfferPayedByFilterType.by_master.value, True),
    (OfferPayedByFilterType.any.value, False),
])
def test_prepare_payed_by_condition_included(payed_by, non_empty):
    conditions = prepare_conditions(
        {'payed_by': payed_by}
    )

    assert bool(conditions) == non_empty
