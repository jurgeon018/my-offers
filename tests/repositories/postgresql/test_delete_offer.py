import pytest

from my_offers import pg
from my_offers.repositories.postgresql.offer import delete_offers_by_id


@pytest.mark.gen_test
async def test_delete_contracts_by_offer_id(mocker):
    # arrange & act
    await delete_offers_by_id([11])

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers WHERE offer_id = ANY($1::BIGINT[])',
        [11]
    )
