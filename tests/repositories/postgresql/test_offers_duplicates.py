import pytest

from my_offers import pg
from my_offers.repositories.postgresql import delete_offers_duplicates


@pytest.mark.gen_test
async def test_delete_offers_duplicates(mocker):
    # arrange & act
    await delete_offers_duplicates([1, 2])

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers_duplicates WHERE offer_id = ANY($1::BIGINT[])',
        [1, 2],
    )
