import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import pg
from my_offers.repositories.postgresql.offer import get_offers_ids_by_tab


@pytest.mark.gen_test
async def test_get_offer_ids_by_tab():
    # arrange
    result = [
        {'offer_id': 1},
        {'offer_id': 2},
        {'offer_id': 3},
    ]

    expected = [1, 2, 3]

    pg.get().fetch.return_value = future(result)

    # act
    result = await get_offers_ids_by_tab(
        {
            'master_user_id': 111,
            'user_id': 12,
            'status_tab': 'deleted',
        }
    )

    # assert
    with settings_stub(DB_TIMEOUT=3):
        assert result == expected

    pg.get().fetch.assert_called_once_with(
        'SELECT offers.offer_id \nFROM offers \nWHERE offers.master_user_id = $1'
        ' AND offers.user_id = $3 AND offers.status_tab = $2',
        111,
        'deleted',
        12,
        timeout=3,
    )
