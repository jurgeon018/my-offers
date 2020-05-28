import asyncio
import os

from cian_functional_test_utils.pytest_plugin import MockResponse

from tests_functional.utils import load_data


async def test_new_offer_duplicate_notification_consumer(queue_service, pg, notification_center_mock):
    # arrange
    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    notification_center_stub = await notification_center_mock.add_stub(
        method='POST',
        path='/v2/register-notifications/',
        response=MockResponse(),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(1)

    # assert
    request = await notification_center_stub.get_request()
    assert request.data == {'announcementsIds': [173975523]}
