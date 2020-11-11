from datetime import datetime

import pytest
from cian_test_utils import future, v

from my_offers import pg
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarning
from my_offers.repositories.postgresql.offer_relevance_warnings import get_offer_relevance_warnings


@pytest.mark.gen_test
async def test_get_offer_relevance_warnings(mocker):
    # arrange
    pg.get().fetch.return_value = future([
        {
            'offer_id': 1,
            'check_id': '26EE3D06-37C5-46C8-B10F-5E05AFB4D520',
            'created_at': datetime(2020, 3, 30),
            'updated_at': datetime(2020, 3, 30),
            'due_date': datetime(2020, 4, 20),
            'finished': False,
        },
        {
            'offer_id': 2,
            'check_id': '99AB6119-8D1C-44B6-8E99-162F38436332',
            'created_at': datetime(2020, 3, 30),
            'updated_at': datetime(2020, 3, 30),
            'due_date': None,
            'finished': False,
        },
    ])

    # act
    result = await get_offer_relevance_warnings([1, 2, 3])

    # assert
    assert result == v([
        OfferRelevanceWarning(
            offer_id=1,
            check_id='26EE3D06-37C5-46C8-B10F-5E05AFB4D520',
            created_at=datetime(2020, 3, 30),
            updated_at=datetime(2020, 3, 30),
            due_date=datetime(2020, 4, 20),
            finished=False,
        ),
        OfferRelevanceWarning(
            offer_id=2,
            check_id='99AB6119-8D1C-44B6-8E99-162F38436332',
            created_at=datetime(2020, 3, 30),
            updated_at=datetime(2020, 3, 30),
            due_date=None,
            finished=False,
        ),
    ])
