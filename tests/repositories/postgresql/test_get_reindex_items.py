from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.entities import ReindexOfferItem
from my_offers.repositories.postgresql.offers_reindex_queue import get_reindex_items


@pytest.mark.gen_test
async def test_get_reindex_items():
    # arrange
    limit = 5
    pg.get().fetch.return_value = future([{
        'offer_id': 11,
        'created_at': datetime(2020, 3, 12),
        'sync': False,
    }])
    expected = [ReindexOfferItem(offer_id=11, created_at=datetime(2020, 3, 12, 0, 0), sync=False)]

    # act
    result = await get_reindex_items(limit)

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        '\n    with offer_ids as (\n        select\n            offer_id\n        from\n            '
        'offers_reindex_queue\n        where\n            not in_process\n        order by\n            '
        'created_at\n        limit $1\n        for update\n    )\n    update\n        offers_reindex_queue\n    '
        'set\n        in_process = true\n    from\n        offer_ids\n    where\n        '
        'offers_reindex_queue.offer_id = offer_ids.offer_id\n    returning\n        offers_reindex_queue.offer_id, '
        'sync, created_at\n    ',
        limit
    )
