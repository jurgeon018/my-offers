from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.postgresql import delete_offers_duplicates
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicate_for_update


async def test_delete_offers_duplicates(mocker):
    # arrange & act
    await delete_offers_duplicates([1, 2])

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers_duplicates WHERE offer_id = ANY($1::BIGINT[])',
        [1, 2],
    )


async def test_get_offer_duplicate_for_update(mocker):
    # arrange
    pg.get().fetchrow.return_value = future({'offer_id': 1})

    # act
    result = await get_offer_duplicate_for_update()

    # assert
    assert result == 1

    pg.get().fetchrow.assert_called_once_with(
        '\n    select\n        offer_id\n    from\n        offers_duplicates\n    where\n        '
        'updated_at < current_timestamp - interval \'24 hours\'\n    order by\n        updated_at\n    limit 1\n    ',
    )
