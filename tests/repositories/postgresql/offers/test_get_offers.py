import pytest

from my_offers import pg
from my_offers.enums import GetOfferStatusTab
from my_offers.repositories import postgresql


@pytest.mark.gen_test
async def test_get_offers_by_status(mocker):
    # arrange
    status_tab = GetOfferStatusTab.active
    user_id = 123
    limit = 20

    # act
    await postgresql.get_object_models(
        status_tab=status_tab,
        user_id=user_id,
        limit=limit
    )

    # assert
    pg.get().fetch.assert_called_with(
        'SELECT offers.raw_data '
        '\nFROM offers '
        '\nWHERE offers.status_tab = $3 AND offers.master_user_id = $1 '
        '\n LIMIT $2',
        user_id,
        limit,
        status_tab.value,
    )
