import pytest
from cian_test_utils import future

from my_offers.enums import OfferPayedByType
from my_offers.helpers.fields import get_payed_by


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('master_user_id', 'published_user_id', 'publisher_user_id', 'expected'),
    (
        (1, 2, 1, OfferPayedByType.by_master),
        (1, 2, 2, OfferPayedByType.by_agent),
        (1, 2, None, None),
        (None, 1, 1, None),
        (1, 3, 2, None)
    )
)
async def test_get_paid_by(mocker, master_user_id, published_user_id, publisher_user_id, expected):
    # arrange
    offer_id = 1
    mocker.patch(
        'my_offers.helpers.fields.get_offer_publisher_user_id',
        return_value=future(publisher_user_id)
    )

    # act
    result = await get_payed_by(
        master_user_id=master_user_id,
        published_user_id=published_user_id,
        offer_id=offer_id
    )

    # assert
    assert result == expected
