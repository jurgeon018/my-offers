from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time

from my_offers import pg
from my_offers.enums import OfferStatusTab
from my_offers.repositories import postgresql


@pytest.mark.gen_test
async def test_set_offers_status_tab():
    # arrange
    now = datetime.now(tz=pytz.UTC)
    offers_ids = [
        1,
        2,
        3
    ]

    # act
    with freeze_time(now):
        await postgresql.set_offers_status_tab(
            offers_ids=offers_ids,
            status_tab=OfferStatusTab.deleted,
        )

    # assert
    pg.get().execute.assert_called_once_with(
        'UPDATE offers SET status_tab=$4, updated_at=$5 WHERE offers.offer_id IN ($1, $2, $3)',
        1, 2, 3,
        OfferStatusTab.deleted.value,
        now
    )
