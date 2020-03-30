from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.postgresql.offer import get_offers_update_at


@pytest.mark.gen_test
async def test_get_offers_update_at(mocker):
    # arrange
    pg.get().fetch.return_value = future([{'offer_id': 1, 'updated_at': datetime(2020, 3, 30)}])
    expected = {1: datetime(2020, 3, 30)}

    # act
    result = await get_offers_update_at([1, 2])

    # assert
    assert result == expected
