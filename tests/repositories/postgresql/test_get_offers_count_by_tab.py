import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import pg
from my_offers.repositories.postgresql.offer import get_offers_count_by_tab


@pytest.mark.gen_test
async def test_get_offer_counters():
    # arrange
    count = 100500

    pg.get().fetchval.return_value = future(count)

    # act
    result = await get_offers_count_by_tab(
        {
            'master_user_id': 111,
            'user_id': 12,
            'status_tab': 'deleted',
        }
    )

    # assert
    with settings_stub(DB_TIMEOUT=3):
        assert result == count

    pg.get().fetchval.assert_called_once_with(
        'SELECT count(*) AS count_1 \nFROM offers \nWHERE offers.master_user_id = $1'
        ' AND offers.user_id = $3 AND offers.status_tab = $2',
        111,
        'deleted',
        12,
        timeout=3,
    )
