import pytest

from my_offers.enums import OfferPayedBy
from my_offers.helpers.fields import _get_offer_payed_by


@pytest.mark.parametrize('master_id, user_id, payed_by, expected', [
    (1, 2, 1, OfferPayedBy.by_master),
    (2, 1, 1, OfferPayedBy.by_agent),
    (1, 2, 3, None),
    (1, 2, None, None),
])
def test_get_offer_payed_by(master_id, user_id, payed_by, expected):
    # act
    result = _get_offer_payed_by(master_id, user_id, payed_by)
    
    # arrange
    assert result == expected
