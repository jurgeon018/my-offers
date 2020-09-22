import pytest
from simple_settings.utils import settings_stub

from my_offers.enums import OfferPayedByFilterType
from my_offers.repositories.postgresql.offer_conditions import prepare_conditions


@pytest.mark.parametrize('toggle, expected_called',[
    (True, True),
    (False, False)
])
def test_prepare_payed_by_condition_call(mocker, toggle, expected_called):
    _prepare_payed_by_condition =  mocker.patch('my_offers.repositories.postgresql.offer_conditions'
    '._prepare_payed_by_condition')

    with settings_stub(ENABLE_PAYED_BY_FILTERS=toggle):
        prepare_conditions(
            {'payed_by': 'any'}
        )

    assert _prepare_payed_by_condition.called == expected_called

@pytest.mark.parametrize('payed_by, included',[
    (OfferPayedByFilterType.by_agent, True),
    (OfferPayedByFilterType.by_master, True),
    (OfferPayedByFilterType.any, False),
])
def test_prepare_payed_by_condition_included(payed_by, included):
    with settings_stub(ENABLE_PAYED_BY_FILTERS=True):
        conditions = prepare_conditions(
            {'payed_by': payed_by}
        )

    assert bool(conditions) == included
