import pytest
from cian_test_utils import future

from my_offers.enums import OfferPayedByType
from my_offers.helpers.fields import get_payed_by


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('publisher_user_id', 'expected'),
    (
        (1, 1),
        (None, None),
    )
)
async def test_get_paid_by(mocker, publisher_user_id, expected):
    # arrange
    offer_id = 1
    mocker.patch(
        'my_offers.helpers.fields.get_offer_publisher_user_id',
        return_value=future(publisher_user_id)
    )

    # act
    result = await get_payed_by(
        offer_id=offer_id
    )

    # assert
    assert result == expected
