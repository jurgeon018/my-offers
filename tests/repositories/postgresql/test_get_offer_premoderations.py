import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.postgresql.offer_premoderation import get_offer_premoderations


@pytest.mark.gen_test
async def test_get_offer_premoderations(mocker):
    # arrange
    pg.get().fetch.return_value = future([{'offer_id': 1}, {'offer_id': 2}])

    # act
    result = await get_offer_premoderations([1, 2, 3])

    # assert
    assert result == [1, 2]
