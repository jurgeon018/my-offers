import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import entities, pg
from my_offers.repositories.postgresql import get_offers_creation_date


@pytest.mark.gen_test
async def test_get_offers_creation_date(mocker):
    # arrange
    pg.get().fetch.return_value = future([{'offer_id': 22, 'creation_date': None}])
    expected = [entities.OfferCreationDate(offer_id=22, creation_date=None)]

    # act
    with settings_stub(DB_TIMEOUT=3):
        result = await get_offers_creation_date(master_user_id=1, offer_ids=[22])

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        '\n    SELECT\n        offer_id,\n        raw_data->>\'creationDate\' as creation_date\n    '
        'FROM\n        offers\n    WHERE\n        master_user_id = $1\n        AND offer_id = ANY($2::BIGINT[])\n    ',
        1,
        [22],
        timeout=3,
    )
