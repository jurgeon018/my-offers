import pytest

from my_offers import pg
from my_offers.repositories.postgresql.offers_reindex_queue import delete_reindex_items


@pytest.mark.gen_test
async def test_delete_reindex_items(mocker):
    # arrange & act
    await delete_reindex_items([11])

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers_reindex_queue WHERE offer_id = ANY($1::BIGINT[])',
        [11]
    )
