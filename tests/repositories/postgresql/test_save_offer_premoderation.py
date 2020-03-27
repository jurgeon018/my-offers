import pytest
import pytz
from freezegun import freeze_time
from freezegun.api import FakeDatetime

from my_offers import pg
from my_offers.entities.moderation import OfferPremoderation
from my_offers.repositories.postgresql.offer_premoderation import save_offer_premoderation


@pytest.mark.gen_test
@freeze_time('2020-03-27')
async def test_save_offer_premoderation(mocker):
    # arrange
    offer_premoderation = OfferPremoderation(
        offer_id=111,
        removed=False,
        row_version=1,
    )

    # act
    await save_offer_premoderation(offer_premoderation)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_premoderations (offer_id, removed, row_version, created_at) VALUES ($2, $4, $5, $1) '
        'ON CONFLICT (offer_id) DO UPDATE SET removed = excluded.removed, row_version = excluded.row_version, '
        'updated_at = $3 WHERE offers_premoderations.row_version < excluded.row_version',
        FakeDatetime(2020, 3, 27, 0, 0, tzinfo=pytz.UTC),
        111,
        FakeDatetime(2020, 3, 27, 0, 0, tzinfo=pytz.UTC),
        False,
        1,
    )
