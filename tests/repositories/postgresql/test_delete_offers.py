import freezegun
import pytest
import pytz
from freezegun.api import FakeDatetime

from my_offers import enums, pg
from my_offers.repositories.postgresql.offer import delete_offers_older_than
from tests.utils import load_data


@pytest.mark.gen_test
@freezegun.freeze_time('2020-03-05 09:00:00.303690+00:00')
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
        FakeDatetime(2020, 2, 24, 9, 0, 0, 303690, pytz.UTC)
    )
