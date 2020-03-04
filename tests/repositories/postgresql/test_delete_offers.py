import pytest

from my_offers import enums, pg
from my_offers.repositories.postgresql.offer import delete_offers_older_than
from tests.utils import load_data


@pytest.mark.gen_test
async def test_save_offer(mocker):
    # arrange
    days_count = 10
    offer_status = enums.OfferStatusTab.deleted.name

    # act
    await delete_offers_older_than(days_count)

    # assert
    pg.get().execute.assert_called_once_with(
        load_data(__file__, 'delete_offers.sql'),
        offer_status,
        days_count
    )
