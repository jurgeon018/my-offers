from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.entities import ReindexOffer
from my_offers.repositories.postgresql.offer import get_offers_for_reindex


@pytest.mark.gen_test
async def test_get_offers_for_reindex(mocker):
    # arrange
    expected = [ReindexOffer(
        offer_id=11,
        raw_data={'offerId': 11},
        updated_at=datetime(2020, 3, 12, 0, 0)
    )]
    pg.get().fetch.return_value = future([{
        'offer_id': 11,
        'raw_data': {'offerId': 11},
        'updated_at': datetime(2020, 3, 12),
    }])

    # act
    result = await get_offers_for_reindex([11])

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        'SELECT offer_id, raw_data, updated_at FROM offers WHERE offer_id = ANY($1::BIGINT[])',
        [11]
    )
