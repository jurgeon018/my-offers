import asyncio

import pytest

from tests.utils import load_json_data


@pytest.mark.parametrize('offer', [
    load_json_data(__file__, 'announcement_similar.json')
])
async def test_process_announcement_consumer__similar_save(queue_service, pg, offer):
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers_similars_flat ORDER BY offer_id DESC LIMIT 1')

    assert row['offer_id'] == 236954116
