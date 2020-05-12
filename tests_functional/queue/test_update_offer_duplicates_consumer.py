import asyncio
import os

import pytest
from cian_functional_test_utils.pytest_plugin import MockResponse

from tests_functional.utils import load_data


@pytest.mark.asyncio
async def test_update_offer_duplicates_consumer(queue_service, pg, offers_duplicates_mock):
    # arrange
    await pg.execute(load_data(os.path.dirname(__file__) + '/../', 'offers.sql'))
    await offers_duplicates_mock.add_stub(
        method='POST',
        path='/v1/get-offers-duplicates-by-ids/',
        response=MockResponse(
            body={
                'duplicates': [{
                    'duplicate_group_id': 1,
                    'offer_id': 209194477,
                }]
            },
        ),
    )

    message = {
        'force': True,
        'id': 209194477,
        'date': '2020-04-29 15:23:00',
    }

    # act
    await queue_service.wait_consumer('my-offers.update_offer_duplicates')
    await queue_service.publish('offer.v1.need-update-duplicate', message, exchange='ml-ranking-dubli')
    await asyncio.sleep(0.5)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers_duplicates WHERE offer_id = 209194477')
    assert row['group_id'] == 1
