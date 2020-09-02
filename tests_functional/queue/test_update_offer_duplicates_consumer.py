import asyncio
from pathlib import Path

import pytest
from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_update_offer_duplicates_consumer(queue_service, pg, runtime_settings, offers_duplicates_mock):
    # arrange
    await runtime_settings.set({'SEND_PUSH_ON_NEW_DUPLICATE': True})
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date) '
        'VALUES(209194477, \'sale\', \'2020-08-10\')'
    )
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
    queue = await queue_service.make_tmp_queue(routing_key='my-offers.offer-duplicate.v1.new')

    message = {
        'force': True,
        'id': 209194477,
        'date': '2020-04-29 15:23:00',
    }

    # act
    await queue_service.wait_consumer('my-offers.update_offer_duplicates')
    await queue_service.publish('offer.v1.need-update-duplicate', message, exchange='ml-ranking-dubli')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers_duplicates WHERE offer_id = 209194477')
    assert row['group_id'] == 1

    row = await pg.fetchrow('SELECT * FROM offers_similars_flat WHERE offer_id = 209194477')
    assert row['group_id'] == 1

    messages = await queue.get_messages()
    assert len(messages) == 1
    assert messages[0].payload['duplicateOfferId'] == 209194477


async def test_update_offer_duplicates_consumer__bad_duplicate__skip(
        queue_service,
        pg,
        runtime_settings,
        offers_duplicates_mock
):
    # arrange
    await runtime_settings.set({
        'SEND_PUSH_ON_NEW_DUPLICATE': True,
        'DUPLICATE_CHECK_ENABLED': True,
    })
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, district_id, sort_date) '
        'VALUES(209194477, \'sale\', 1, \'2020-08-10\')'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, group_id, district_id, sort_date) '
        'VALUES(2, \'sale\', 1, 2, \'2020-08-10\')'
    )

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
    queue = await queue_service.make_tmp_queue(routing_key='my-offers.offer-duplicate.v1.new')

    message = {
        'force': True,
        'id': 209194477,
        'date': '2020-04-29 15:23:00',
    }

    # act
    await queue_service.wait_consumer('my-offers.update_offer_duplicates')
    await queue_service.publish('offer.v1.need-update-duplicate', message, exchange='ml-ranking-dubli')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers_duplicates WHERE offer_id = 209194477')
    assert row['group_id'] == 1

    row = await pg.fetchrow('SELECT * FROM offers_similars_flat WHERE offer_id = 209194477')
    assert row['group_id'] is None

    messages = await queue.get_messages()
    assert len(messages) == 0


async def test_update_offer_duplicates_consumer__has_duplicate__not_message(
        queue_service,
        runtime_settings,
        pg,
        offers_duplicates_mock,
):
    # arrange
    await runtime_settings.set({'SEND_PUSH_ON_NEW_DUPLICATE': True})

    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates VALUES(209194477, 209194477, \'2020-05-13\')')
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

    queue = await queue_service.make_tmp_queue(routing_key='my-offers.offer-duplicate.v1.new')

    # act
    await queue_service.wait_consumer('my-offers.update_offer_duplicates')
    await queue_service.publish('offer.v1.need-update-duplicate', message, exchange='ml-ranking-dubli')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers_duplicates WHERE offer_id = 209194477')
    assert row['group_id'] == 1

    messages = await queue.get_messages()
    assert len(messages) == 0


async def test_update_offer_duplicates_consumer__not_duplicate__delete(queue_service, pg, offers_duplicates_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates VALUES(209194477, 209194477, \'2020-05-13\')')
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, group_id, sort_date) '
        'VALUES(209194477, \'sale\', 1, \'2020-08-10\')'
    )
    await offers_duplicates_mock.add_stub(
        method='POST',
        path='/v1/get-offers-duplicates-by-ids/',
        response=MockResponse(
            body={
                'duplicates': []
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
    assert row is None

    row = await pg.fetchrow('SELECT * FROM offers_similars_flat WHERE offer_id = 209194477')
    assert row['group_id'] is None
