import pytest

from my_offers.entities import OfferActionRequest, OfferActionResponse
from my_offers.enums.offer_action_status import OfferActionStatus
from my_offers.services.actions import archive_offer


@pytest.mark.gen_test
async def test_archive_offer(mocker):
    # arrange
    expected = OfferActionResponse(status=OfferActionStatus.ok)

    # act
    result = await archive_offer(OfferActionRequest(offer_id=11), 555)

    # assert
    assert result == expected
