from datetime import datetime

import pytest
import pytz

from my_offers import pg
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarning
from my_offers.repositories.postgresql.offer_relevance_warnings import save_offer_relevance_warning


@pytest.mark.gen_test
async def test_save_offer_relevance_warning():
    # arrange
    offer_relevance_warning = OfferRelevanceWarning(
        offer_id=111,
        check_id='C919B985-489B-4033-B74B-8F8A934B8192',
        created_at=datetime(2020, 3, 30, tzinfo=pytz.UTC),
        updated_at=datetime(2020, 3, 30, tzinfo=pytz.UTC),
        due_date=datetime(2020, 4, 20, tzinfo=pytz.UTC),
        finished=False,
    )

    # act
    await save_offer_relevance_warning(offer_relevance_warning)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offer_relevance_warnings (offer_id, check_id, finished, due_date, created_at, updated_at) '
        'VALUES ($5, $1, $4, $3, $2, $6) ON CONFLICT (offer_id) DO UPDATE SET '
        'check_id = excluded.check_id, finished = excluded.finished, '
        'due_date = excluded.due_date, updated_at = excluded.updated_at',
        'C919B985-489B-4033-B74B-8F8A934B8192',
        datetime(2020, 3, 30, 0, 0, tzinfo=pytz.UTC),
        datetime(2020, 4, 20, 0, 0, tzinfo=pytz.UTC),
        False,
        111,
        datetime(2020, 3, 30, 0, 0, tzinfo=pytz.UTC),
    )
